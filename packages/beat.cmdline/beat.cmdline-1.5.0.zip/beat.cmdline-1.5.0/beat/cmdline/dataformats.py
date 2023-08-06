#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###################################################################################
#                                                                                 #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/               #
# Contact: beat.support@idiap.ch                                                  #
#                                                                                 #
# Redistribution and use in source and binary forms, with or without              #
# modification, are permitted provided that the following conditions are met:     #
#                                                                                 #
# 1. Redistributions of source code must retain the above copyright notice, this  #
# list of conditions and the following disclaimer.                                #
#                                                                                 #
# 2. Redistributions in binary form must reproduce the above copyright notice,    #
# this list of conditions and the following disclaimer in the documentation       #
# and/or other materials provided with the distribution.                          #
#                                                                                 #
# 3. Neither the name of the copyright holder nor the names of its contributors   #
# may be used to endorse or promote products derived from this software without   #
# specific prior written permission.                                              #
#                                                                                 #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED   #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE    #
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL      #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR      #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER      #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.            #
#                                                                                 #
###################################################################################


import logging
import click

from beat.core import dataformat


from . import common
from . import commands

from .decorators import raise_on_error
from .click_helper import AliasedGroup

logger = logging.getLogger(__name__)


def pull_impl(webapi, prefix, names, force, indentation, cache):
    """Copies dataformats (recursively) from the server.

  Data formats are particularly tricky to download because of their recursive
  nature. This requires a specialized recursive technique to download base and
  referenced dataformats.


  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    names (:py:class:`list`): A list of strings, each representing the unique
      relative path of the objects to retrieve or a list of usernames from
      which to retrieve objects. If the list is empty, then we pull all
      available objects of a given type. If no user is set, then pull all
      public objects of a given type.

    force (bool): If set to ``True``, then overwrites local changes with the
      remotely retrieved copies.

    indentation (int): The indentation level, useful if this function is called
      recursively while downloading different object types. This is normally
      set to ``0`` (zero).

    cache (dict): A dictionary containing all dataformats already downloaded.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    dataformats = set(names)  # what is being request
    download = dataformats - set(cache.keys())  # what we actually need

    if not download:
        return 0

    status, downloaded = common.pull(
        webapi,
        prefix,
        "dataformat",
        download,
        ["declaration", "description"],
        force,
        indentation,
    )

    if status != 0:
        return status

    if indentation == 0:
        indentation = 4

    # see what else one needs to pull
    for name in downloaded:
        try:
            obj = dataformat.DataFormat(prefix, name)
            cache[name] = obj
            if not obj.valid:
                cache[name] = None

            # downloads any dependencies
            dataformats |= obj.referenced.keys()

        except Exception as e:
            logger.error("loading `%s': %s...", name, str(e))
            cache[name] = None

    # recurse until done
    return pull_impl(webapi, prefix, dataformats, force, 2 + indentation, cache)


@click.group(cls=AliasedGroup)
@click.pass_context
def dataformats(ctx):
    """Configuration manipulation of data formats"""

    ctx.meta["asset_type"] = "dataformat"
    ctx.meta["diff_fields"] = ["declaration", "description"]


CMD_LIST = [
    "list",
    "path",
    "edit",
    "check",
    "status",
    "create",
    "version",
    "fork",
    "rm",
    "diff",
]

commands.initialise_asset_commands(dataformats, CMD_LIST)


@dataformats.command()
@click.argument("name", nargs=-1)
@click.option(
    "--force", help="Performs operation regardless of conflicts", is_flag=True
)
@click.pass_context
@raise_on_error
def pull(ctx, name, force):
    """Downloads the specified dataformats from the server

  Example:
    $ beat dataformats pull --force yyy
  """
    with common.make_webapi(ctx.meta["config"]) as webapi:
        name = common.make_up_remote_list(webapi, "dataformat", name)
        if name is None:
            return 1  # error
        return pull_impl(webapi, ctx.meta["config"].path, name, force, 0, {})


@dataformats.command()
@click.argument("name", nargs=-1)
@click.option(
    "--force", help="Performs operation regardless of conflicts", is_flag=True
)
@click.option(
    "--dry-run",
    help="Doesn't really perform the task, just " "comments what would do",
    is_flag=True,
)
@click.pass_context
@raise_on_error
def push(ctx, name, force, dry_run):
    """Uploads dataformats to the server

  Example:
    $ beat dataformats push --dry-run yyy
  """
    with common.make_webapi(ctx.meta["config"]) as webapi:
        return common.push(
            webapi,
            ctx.meta["config"].path,
            "dataformat",
            name,
            ["name", "declaration", "description"],
            {},
            force,
            dry_run,
            0,
        )
