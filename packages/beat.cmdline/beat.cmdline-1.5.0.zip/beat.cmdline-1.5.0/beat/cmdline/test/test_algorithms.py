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


# Basic tests for the command line beat program: algorithms

import nose.tools
from click.testing import CliRunner

from beat.core.test.utils import slow, cleanup, skipif
from beat.core.algorithm import Storage
from beat.core.dataformat import Storage as DFStorage

from beat.cmdline.scripts import main_cli

from . import core
from . import platform, disconnected, prefix, tmp_prefix, user, token


def setup():
    """Create default dataformat for algorithm prototype loading"""

    from .test_dataformats import call as df_call

    obj = "user/integers/1"

    storage = DFStorage(tmp_prefix, obj)

    if not storage.exists():
        nose.tools.eq_(df_call("create", obj, prefix=tmp_prefix), 0)
        if not disconnected:
            nose.tools.eq_(df_call("push", obj, prefix=tmp_prefix), 0)


def call(*args, **kwargs):
    """A central mechanism to call the main routine with the right parameters"""

    use_prefix = kwargs.get("prefix", prefix)
    use_platform = kwargs.get("platform", platform)
    use_cache = kwargs.get("cache", "cache")

    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            main_cli.main,
            [
                "--platform",
                use_platform,
                "--user",
                user,
                "--token",
                token,
                "--prefix",
                use_prefix,
                "--cache",
                use_cache,
                "--test-mode",
                "algorithms",
            ]
            + list(args),
            catch_exceptions=False,
        )
        return result.exit_code, result.output


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_remote_list():
    exit_code, outputs = call("list", "--remote")
    nose.tools.eq_(exit_code, 0, msg=outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_one():
    obj = "user/integers_add/1"
    exit_code, outputs = call("pull", obj, prefix=tmp_prefix)
    nose.tools.eq_(exit_code, 0, outputs)
    s = Storage(tmp_prefix, obj)
    nose.tools.assert_true(s.exists())


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_all():
    exit_code, outputs = call("pull", prefix=tmp_prefix)
    nose.tools.eq_(exit_code, 0, outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_diff():
    obj = "user/integers_add/1"
    exit_code, outputs = call("pull", obj, prefix=tmp_prefix)
    nose.tools.eq_(exit_code, 0, outputs)

    # quickly modify the user algorithm by emptying it
    storage = Storage(tmp_prefix, obj)
    storage.code.save("class Algorithm:\n  pass")

    exit_code, outputs = call("diff", obj, prefix=tmp_prefix)
    nose.tools.eq_(exit_code, 0, outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_status():
    test_diff()
    test_pull_one()
    exit_code, outputs = call("status", prefix=tmp_prefix)
    nose.tools.eq_(exit_code, 0, outputs)


@nose.tools.with_setup(setup=setup, teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_push_and_delete():
    obj = "user/newobject/1"
    TestAlgorithmLocal.create(obj)

    # now push the new object and then delete it remotely
    exit_code, outputs = call("push", obj, prefix=tmp_prefix)
    nose.tools.eq_(exit_code, 0, outputs)
    exit_code, outputs = call("rm", "--remote", obj, prefix=tmp_prefix)
    nose.tools.eq_(exit_code, 0, outputs)


class TestAlgorithmLocal(core.AssetLocalTest):
    storage_cls = Storage
    asset_type = "algorithm"
    object_map = {
        "valid": "legacy/valid_algorithm/1",
        "invalid": "user/invalid/1",
        "create": "legacy/new_algorithm/1",
        "new": "legacy/new_algorithm/2",
        "fork": "legacy/forked_algorithm/1",
    }

    def setup(self):
        obj = "user/integers/1"
        storage = DFStorage(tmp_prefix, obj)
        if not storage.exists():
            exit_code, outputs = self.call(
                "create", obj, prefix=tmp_prefix, asset_type="dataformat"
            )
            nose.tools.eq_(exit_code, 0, outputs)
            if not disconnected:
                exit_code, outputs = self.call(
                    "push", obj, prefix=tmp_prefix, asset_type="dataformat"
                )
                nose.tools.eq_(exit_code, 0, outputs)
