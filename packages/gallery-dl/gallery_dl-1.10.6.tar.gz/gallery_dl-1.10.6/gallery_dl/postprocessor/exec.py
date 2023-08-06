# -*- coding: utf-8 -*-

# Copyright 2018-2019 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Execute processes"""

from .common import PostProcessor
from .. import util
import subprocess
import os


if os.name == "nt":
    def quote(s):
        return '"' + s.replace('"', '\\"') + '"'
else:
    from shlex import quote


class ExecPP(PostProcessor):

    def __init__(self, pathfmt, options):
        PostProcessor.__init__(self)
        args = options["command"]

        if isinstance(args, str):
            if "{}" not in args:
                args += " {}"
            self.args = args
            self.shell = True
            self._format = self._format_args_string
        else:
            self.args = [util.Formatter(arg) for arg in args]
            self.shell = False
            self._format = self._format_args_list

        if options.get("async", False):
            self._exec = self._exec_async

    def run_after(self, pathfmt):
        self._exec(self._format(pathfmt))

    def _format_args_string(self, pathfmt):
        return self.args.replace("{}", quote(pathfmt.realpath))

    def _format_args_list(self, pathfmt):
        kwdict = pathfmt.kwdict
        kwdict["_directory"] = pathfmt.realdirectory
        kwdict["_filename"] = pathfmt.filename
        kwdict["_path"] = pathfmt.realpath
        return [arg.format_map(kwdict) for arg in self.args]

    def _exec(self, args):
        self.log.debug("Running '%s'", args)
        retcode = subprocess.Popen(args, shell=self.shell).wait()
        if retcode:
            self.log.warning(
                "Executing '%s' returned with non-zero exit status (%d)",
                " ".join(args) if isinstance(args, list) else args, retcode)

    def _exec_async(self, args):
        subprocess.Popen(args, shell=self.shell)


__postprocessor__ = ExecPP
