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


# Basic tests for the command line beat program: dataformats

import nose.tools
import click
from click.testing import CliRunner

from beat.cmdline.scripts import main_cli
from beat.core.test.utils import slow, cleanup, skipif
from beat.core.dataformat import Storage, DataFormat

from . import core
from . import platform, disconnected, prefix, tmp_prefix, user, token


def call(*args, **kwargs):
    """A central mechanism to call the main routine with the right parameters"""

    use_prefix = kwargs.get("prefix", prefix)
    use_platform = kwargs.get("platform", platform)

    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            main_cli.main,
            [
                "--test-mode",
                "--prefix",
                use_prefix,
                "--token",
                token,
                "--user",
                user,
                "--platform",
                use_platform,
                "dataformats",
            ]
            + list(args),
            catch_exceptions=False,
        )
    if result.exit_code != 0:
        click.echo(result.output)
    return result.exit_code


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_remote_list():
    nose.tools.eq_(call("list", "--remote"), 0)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_one():
    obj = "system/bounding_box_video/1"
    nose.tools.eq_(call("pull", obj, prefix=tmp_prefix), 0)
    s = Storage(tmp_prefix, obj)
    nose.tools.assert_true(s.exists())


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_all():
    nose.tools.eq_(call("pull", prefix=tmp_prefix), 0)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_diff():
    obj = "system/integer/1"
    nose.tools.eq_(call("pull", obj, prefix=tmp_prefix), 0)

    # quickly modify the user dataformat by emptying it
    f = DataFormat(tmp_prefix, obj)
    f.data["value"] = "int64"
    f.write()

    nose.tools.eq_(call("diff", obj, prefix=tmp_prefix), 0)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_status():
    test_diff()
    test_pull_one()
    nose.tools.eq_(call("status", prefix=tmp_prefix), 0)


@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_push_and_delete():
    obj = "user/newobject/1"
    TestDataFormatLocal.create(obj)

    # now push the new object and then delete it remotely
    nose.tools.eq_(call("push", obj, prefix=tmp_prefix), 0)
    nose.tools.eq_(call("rm", "--remote", obj, prefix=tmp_prefix), 0)


class TestDataFormatLocal(core.AssetLocalTest):
    storage_cls = Storage
    asset_type = "dataformat"
    object_map = {
        "valid": "user/3d_array_of_dataformat/1",
        "invalid": "user/invalid/1",
        "create": "user/new_dataformat/1",
        "new": "user/new_dataformat/2",
        "fork": "user/forked_dataformat/1",
    }
