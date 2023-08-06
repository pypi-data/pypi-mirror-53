#!/usr/bin/env python
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


def catchall():
    from . import _x as x
    from . import _root_parser
    from .common import edie

    if isinstance(x.action, str):
        edie('didn\'t recognize that request\n\n'
             '{}'.format(_root_parser.print_usage()))

    if callable(x.action):
        print(x.action())
    else:
        print(x.action)

    raise SystemExit


def main():
    import os
    from . import _x as x
    from . import _commands, _root_parser, new_xanity_session
    from .common import find_xanity_root, edie
    from .xanity_env import correct_environment

    if x.args.version:
        from . import __version__ as version

        print(version)
        raise SystemExit(0)

    if x.args.xanity_root:
        root = find_xanity_root(x.args.xanity_root)
        os.chdir(root)
        x = new_xanity_session()

    if 'help' in x.args.action:
        _root_parser.print_help()
        raise SystemExit(0)

    if x.action is None:
        edie(_root_parser.print_usage())

    if x.action not in _commands.init:
        if find_xanity_root(os.getcwd()) is None:
            edie('Get in a xanity project tree, or use the --directory (-d) option to specify one.')

    if x.action == _commands.sesh:
        _commands.sesh.entry()

    if x.action in _commands.run:
        correct_environment()

    if x.action in _commands:
        _commands[x.action].entry()
    else:
        catchall()

    raise SystemExit(0)


if __name__ == '__main__':
    main()
