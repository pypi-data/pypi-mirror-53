from __future__ import absolute_import, division, print_function

import os
import subprocess
import argparse

import ctl
import ctl.config
import select
import confu.schema

from ctl.auth import expose
from ctl.plugins import command
from ctl.exceptions import UsageError

import ctl.plugins.repository
import ctl.plugins.git


class ReleasePluginConfig(confu.schema.Schema):
    target = confu.schema.Str(
        help="target for release - should be a path "
        "to a python package or the name of a "
        "repository type plugin",
        cli=False,
        default=None,
    )


class ReleasePlugin(command.CommandPlugin):

    """
    base plugin interface for releasing / packaging software
    """

    class ConfigSchema(ctl.plugins.PluginBase.ConfigSchema):
        config = ReleasePluginConfig()

    @classmethod
    def add_arguments(cls, parser, plugin_config):

        shared_parser = argparse.ArgumentParser(add_help=False)
        group = shared_parser.add_argument_group()

        group.add_argument(
            "version",
            nargs=1,
            type=str,
            help="release version - if target is managed by git, "
            "checkout this branch/tag",
        )

        group.add_argument(
            "target",
            nargs="?",
            type=str,
            default=plugin_config.get("target"),
            help=ReleasePluginConfig().target.help,
        )

        sub = parser.add_subparsers(title="Operation", dest="op")

        op_release_parser = sub.add_parser(
            "release", help="execute release", parents=[shared_parser]
        )

        op_release_parser.add_argument(
            "--dry", action="store_true", help="Do a dry run (nothing will be uploaded)"
        )

        op_validate_parser = sub.add_parser(
            "validate", help="validate release", parents=[shared_parser]
        )

        return {
            "group": group,
            "confu_target": op_release_parser,
            "op_release_parser": op_release_parser,
            "op_validate_parser": op_validate_parser,
        }

    def execute(self, **kwargs):
        self.kwargs = kwargs
        self.prepare()
        self.shell = True

        self.set_target(self.get_config("target"))
        self.dry_run = kwargs.get("dry")
        self.version = kwargs.get("version")[0]
        self.orig_branch = self.target.branch

        if self.dry_run:
            self.log.info("Doing dry run...")
        self.log.info("Release target: {}".format(self.target))

        try:
            self.target.checkout(self.version)
            op = self.get_op(kwargs.get("op"))
            op(**kwargs)
        finally:
            self.target.checkout(self.orig_branch)

    def set_target(self, target):
        if not target:
            raise ValueError("No target specified")

        try:
            self.target = self.other_plugin(target)
            if not isinstance(self.target, ctl.plugins.repository.RepositoryPlugin):
                raise TypeError(
                    "The plugin with the name `{}` is not a "
                    "repository type plugin and cannot be used "
                    "as a target".format(target)
                )
        except KeyError:
            self.target = os.path.abspath(target)
            if not os.path.exists(self.target):
                raise IOError(
                    "Target is neither a configured repository "
                    "plugin nor a valid file path: "
                    "{}".format(self.target)
                )

            self.target = ctl.plugins.git.temporary_plugin(
                self.ctl, "{}__tmp_repo".format(self.plugin_name), self.target
            )

        self.cwd = self.target.checkout_path

    @expose("ctl.{plugin_name}.release")
    def release(self, **kwargs):
        self._release(**kwargs)

    @expose("ctl.{plugin_name}.validate")
    def validate(self, **kwargs):
        self._validate(**kwargs)

    def _release(self, **kwargs):
        """ should run release logic """
        raise NotImplementedError()

    def _validate(self, **kwargs):
        """ should run validation logic """
        raise NotImplementedError()
