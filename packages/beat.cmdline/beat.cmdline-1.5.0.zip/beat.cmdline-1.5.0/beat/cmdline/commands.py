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

import click
import types

from .decorators import raise_on_error

from . import common


def copy_func(f, name=None):
    """
    based on https://stackoverflow.com/a/30714299/5843716

    return a function with same code, globals, defaults, closure, doc, and
    name (or provide a new name)
    """
    fn = types.FunctionType(
        f.__code__, f.__globals__, name or f.__name__, f.__defaults__, f.__closure__
    )
    # in case f was given attrs (note this dict is a shallow copy):
    fn.__dict__.update(f.__dict__)
    fn.__doc__ = f.__doc__

    return fn


@click.option(
    "--remote", help="Only acts on the remote copy of the list.", is_flag=True
)
@click.pass_context
@raise_on_error
def list_impl(ctx, remote):
    """Lists the assets of this type available on the platform.

    To list all existing asset of a type on your local prefix:

    $ beat <asset_type> list
    """

    if remote:
        with common.make_webapi(ctx.meta["config"]) as webapi:
            return common.display_remote_list(webapi, ctx.meta["asset_type"])
    else:
        return common.display_local_list(
            ctx.meta["config"].path, ctx.meta["asset_type"]
        )


@click.argument("names", nargs=-1)
@click.pass_context
@raise_on_error
def path_impl(ctx, names):
    """Displays local path of asset files

  Example:
    $ beat <asset_type> path xxx
  """

    return common.display_local_path(
        ctx.meta["config"].path, ctx.meta["asset_type"], names
    )


@click.argument("name", nargs=1)
@click.pass_context
@raise_on_error
def edit_impl(ctx, name):
    """Edit local asset file

  Example:
    $ beat <asset_type> edit xxx
  """

    return common.edit_local_file(
        ctx.meta["config"].path, ctx.meta["config"].editor, ctx.meta["asset_type"], name
    )


@click.argument("names", nargs=-1)
@click.pass_context
@raise_on_error
def check_impl(ctx, names):
    """Checks a local asset for validity.

    Example:
      $ beat <asset_type> check xxx
    """

    return common.check(ctx.meta["config"].path, ctx.meta["asset_type"], names)


@click.pass_context
@raise_on_error
def status_impl(ctx):
    """Shows (editing) status for all available items of asset type

  Example:
    $ beat <asset_type> status
  """

    config = ctx.meta["config"]
    with common.make_webapi(config) as webapi:
        return common.status(webapi, config.path, ctx.meta["asset_type"])[0]


@click.argument("names", nargs=-1)
@click.pass_context
@raise_on_error
def create_impl(ctx, names):
    """Creates a new local asset.

    Example:
      $ beat <asset_type> create xxx
    """

    return common.create(ctx.meta["config"].path, ctx.meta["asset_type"], names)


@click.argument("name", nargs=1)
@click.pass_context
@raise_on_error
def version_impl(ctx, name):
    """Creates a new version of an existing asset

    Example:
      $ beat <asset_type> version xxx
    """

    return common.new_version(ctx.meta["config"].path, ctx.meta["asset_type"], name)


@click.argument("src", nargs=1)
@click.argument("dst", nargs=1)
@click.pass_context
@raise_on_error
def fork_impl(ctx, src, dst):
    """Forks a local asset

    Example:
      $ beat <asset_type> fork xxx yyy
    """

    return common.fork(ctx.meta["config"].path, ctx.meta["asset_type"], src, dst)


@click.argument("name", nargs=-1)
@click.option(
    "--remote", help="Only acts on the remote copy of the algorithm", is_flag=True
)
@click.pass_context
@raise_on_error
def rm_impl(ctx, name, remote):
    """Deletes a local asset (unless --remote is specified)

    Example:
      $ beat <asset_type> rm xxx
    """

    config = ctx.meta["config"]
    asset_type = ctx.meta["asset_type"]

    if remote:
        with common.make_webapi(config) as webapi:
            return common.delete_remote(webapi, asset_type, name)
    else:
        return common.delete_local(config.path, asset_type, name)


@click.argument("name", nargs=-1)
@click.pass_context
@raise_on_error
def rm_local_impl(ctx, name):
    """Deletes a local asset

    Example:
      $ beat <asset_type> rm xxx
    """

    return common.delete_local(ctx.meta["config"].path, ctx.meta["asset_type"], name)


@click.argument("name", nargs=1)
@click.pass_context
@raise_on_error
def diff_impl(ctx, name):
    """Shows changes between the local dataformat and the remote version

    Example:
      $ beat toolchains diff xxx
    """

    config = ctx.meta["config"]

    with common.make_webapi(config) as webapi:
        return common.diff(
            webapi, config.path, ctx.meta["asset_type"], name, ctx.meta["diff_fields"]
        )


CMD_TABLE = {
    "list": list_impl,
    "path": path_impl,
    "edit": edit_impl,
    "check": check_impl,
    "status": status_impl,
    "create": create_impl,
    "version": version_impl,
    "fork": fork_impl,
    "rm": rm_impl,
    "rm_local": rm_local_impl,
    "diff": diff_impl,
}


def command(name):
    """Returns a copy of the method to be decorated.

    This allows to reuse the same commands. Using directly the original method
    would allow to only use it once.

    Parameters:
        name str: Name of the desired command
    """

    return copy_func(CMD_TABLE[name])


def initialise_asset_commands(click_cmd_group, cmd_list):
    """Initialize a command group adding all the commands from cmd_list to it

    Parameters:
        click_cmd_group obj: click command to group
        cmd_list list: list of string or tuple of the commands to add
    """

    for item in cmd_list:
        if isinstance(item, tuple):
            click_cmd_group.command(name=item[0])(command(item[1]))
        else:
            click_cmd_group.command(name=item)(command(item))
