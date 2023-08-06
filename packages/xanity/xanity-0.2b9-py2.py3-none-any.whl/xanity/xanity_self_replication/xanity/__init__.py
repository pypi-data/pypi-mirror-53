# -*- coding: utf-8 -*-
#
# Copyright 2018 Barry Muldrey
#
# This file is part of xanity.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

__version__ = "0.2b9"            # this is the definitive version for distribution
__author__ = "Barry Muldrey"
__copyright__ = "Copyright 2018"
__license__ = "GNU Affero GPL"
__maintainer__ = "Barry Muldrey"
__email__ = "barry@muldrey.net"
__status__ = "Beta"
__credits__ = []

import argparse

from .xanity_data import commands as _data_cmds
from .xanity_run import commands as _run_cmds
from .xanity_env import commands as _env_cmds
from .xanity_init import commands as _init_cmds
from .xanity_develop import commands as _dev_cmds
from .common import RootParser as _RootParser, CommandSet

from .xanity_data import load_data, save_variable, save_path, load_checkpoint, save_checkpoint
from .xanity_data import fetch_timer_data, persistent_variable, persistent_path, timed_fn


class ListParser(argparse.ArgumentParser):
    def __init__(self, *clargs, **kwargs):
        super(ListParser, self).__init__(*clargs, **kwargs)
        self.add_argument('action_object', nargs='?', default=None,
                          help='either "experiments" or "analyses"')


def list_cmd_entry():
    from . import _x as x
    exps = [item[0] for item in list(x.list_avail_experiments())]
    anals = [item[0] for item in list(x.list_avail_analyses())]
    if exps and (x.args.action_object == 'experiments' or x.args.action_object is None):
        print('available_experiments:' + ''.join(['\n    - {}'.format(e) for e in exps]))
    if anals and (x.args.action_object == 'analyses' or x.args.action_object is None):
        print('available_analyses:' + ''.join(['\n    - {}'.format(a) for a in anals]))


_commands = CommandSet([
    (['list'], ListParser, list_cmd_entry, 'list modules xanity can run')
])

_commands = _commands + _data_cmds + _run_cmds + _env_cmds + _init_cmds + _dev_cmds
_root_parser = _RootParser(_commands)


def new_xanity_session():
    global _x
    from .class_obj import XanityClass as _XanityClass

    # have to set placeholders because modules which import
    # xanity might have to be imported during the creation of the Xanity object

    _x = _XanityClass()

    # # the following will replace the 'xanity' module with the _xanity object:
    # del sys.modules['xanity']
    # sys.modules['xanity'] = _xanity

    return _x


if '_x' not in locals():
    _x = new_xanity_session()


# register the import of xanity
_x.register_import()


def experiment_parameters(*args, **kwargs):
    return _x.experiment_parameters(*args, **kwargs)


def log(*args, **kwargs):
    return _x.log(*args, **kwargs)


def run(*args, **kwargs):
    return _x.run(*args, **kwargs)


def cmd(command):
    """USED TO DRIVE XANITY FROM WITH PYTHON COMMANDS"""
    return _x.cmd(command)


def metarun(*args, **kwargs):
    return _x.metarun(*args, **kwargs)


def project_root():
    return _x.paths.project_root


def trials(*args, **kwargs):
    return _x.trials(*args, **kwargs)


def shell_prelude(value=None):
    return _x.shell_prelude
