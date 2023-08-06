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


"""
Base class for asset testing
"""


import nose.tools
import click
from click.testing import CliRunner

from beat.core.test.utils import cleanup
from beat.cmdline.scripts import main_cli

from .. import common

from . import platform, prefix, tmp_prefix, user, token


class AssetLocalTest:
    asset_type = None
    object_map = {}
    storage_cls = None

    def __init__(self):
        nose.tools.assert_true(self.object_map)

    def teardown(self):
        cleanup()

    @classmethod
    def call(cls, *args, **kwargs):
        """A central mechanism to call the main routine with the right parameters"""

        use_prefix = kwargs.get("prefix", prefix)
        use_platform = kwargs.get("platform", platform)
        use_cache = kwargs.get("cache", "cache")
        asset_type = kwargs.get("asset_type", cls.asset_type)

        cmd_group = common.TYPE_PLURAL[asset_type]
        if "/" in cmd_group:
            cmd_group = cmd_group.split("/")[-1]

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
                    "--cache",
                    use_cache,
                    "--platform",
                    use_platform,
                    cmd_group,
                ]
                + list(args),
                catch_exceptions=False,
            )

        if result.exit_code != 0:
            click.echo(result.output)
        return result.exit_code, result.output

    def test_local_list(self):
        exit_code, outputs = self.call("list")
        nose.tools.eq_(exit_code, 0, outputs)

    def test_check_valid(self):
        exit_code, outputs = self.call("check", self.object_map["valid"])
        nose.tools.eq_(exit_code, 0, outputs)

    def test_check_invalid(self):
        exit_code, outputs = self.call("check", self.object_map["invalid"])
        nose.tools.eq_(exit_code, 1, outputs)

    @classmethod
    def create(cls, obj=None):
        obj = obj or cls.object_map["create"]
        exit_code, outputs = cls.call("create", obj, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)
        s = cls.storage_cls(tmp_prefix, obj)
        nose.tools.assert_true(s.exists())
        return s

    def test_create(self, obj=None):
        self.create(self.object_map["create"])

    def test_new_version(self):
        obj = self.object_map["create"]
        obj2 = self.object_map["new"]
        self.test_create(obj)
        exit_code, outputs = self.call("version", obj, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)
        s = self.storage_cls(tmp_prefix, obj2)
        nose.tools.assert_true(s.exists())

        # check version status
        with common.Selector(tmp_prefix) as selector:
            nose.tools.eq_(selector.version_of(self.asset_type, obj2), obj)

    def test_fork(self):
        obj = self.object_map["create"]
        obj2 = self.object_map["fork"]
        self.test_create(obj)
        with common.Selector(tmp_prefix) as selector:
            if selector.can_fork(self.asset_type):
                exit_code, outputs = self.call("fork", obj, obj2, prefix=tmp_prefix)
                nose.tools.eq_(exit_code, 0, outputs)
                selector.load()
                s = self.storage_cls(tmp_prefix, obj2)
                nose.tools.assert_true(s.exists())
                nose.tools.eq_(selector.forked_from(self.asset_type, obj2), obj)
            else:
                exit_code, outputs = self.call("fork", obj, obj2, prefix=tmp_prefix)
                nose.tools.assert_not_equal(exit_code, 0)

    def test_delete_local(self):
        obj = self.object_map["create"]
        storage = self.create(obj)
        exit_code, outputs = self.call("rm", obj, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 0, outputs)
        nose.tools.assert_false(storage.exists())

    def test_delete_local_unexisting(self):
        obj = self.object_map["create"]
        storage = self.storage_cls(tmp_prefix, obj)
        nose.tools.assert_false(storage.exists())

        exit_code, outputs = self.call("rm", obj, prefix=tmp_prefix)
        nose.tools.eq_(exit_code, 1, outputs)
        nose.tools.assert_false(storage.exists())
