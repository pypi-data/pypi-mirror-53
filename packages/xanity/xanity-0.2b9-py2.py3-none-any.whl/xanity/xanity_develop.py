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

import shutil

from .common import *
from .constants import *

helptext = """
develop copy-examples :  copy files in experiments/ and analyses/ into the xanity source skeleton path
and append \'_EXAMPLE\', thus adding them into the included example project

usage:  xanity develop copy-examples

xanity dev assumes you're in a xanity tree (generally speaking)
"""


class DevRootParser(argparse.ArgumentParser):
    def __init__(self):
        from . import _root_parser
        super(DevRootParser, self).__init__(prog='xanity-develop',
                                            description='tools for modifying xanity package source',
                                            parents=[_root_parser],
                                            add_help=False,
                                            )

        self.add_argument('subaction', help='manipulate the internal conda env')

    def parse_known_args(self, *args, **kwargs):
        kn, unk = super(DevRootParser, self).parse_known_args(*args, **kwargs)

        if kn.subaction in subcommands:
            return subcommands[kn.subaction].parser().parse_known_args(*args, **kwargs)
        else:
            return kn, unk


class CopyParser(argparse.ArgumentParser):
    def __init__(self):
        super(CopyParser, self).__init__(prog='xanity-develop-cp',
                                         description='copy files into skeleton project',
                                         parents=[DevRootParser()])
        self.add_argument('files', nargs='*', help='copy file into source skeleton as an \'_EXAMPLE\'')
        self.add_argument('--example', '--examples', '-e', action='store_true')


def cmd_entry_cp():
    from . import _x as x
    from . import __file__ as souce_root

    skel_root = os.path.dirname(souce_root.split('xanity_self_replication')[0])
    skel_root = os.path.join(skel_root, 'skeleton')
    if not os.path.isdir(skel_root):
        edie('can\'t find xanity source')

    proj_root = x.paths.project_root

    if x.debug_xanity:
        print('about to link: {}'.format(x.args.files))

    for f in x.args.files:
        f = os.path.expandvars(os.path.expanduser(os.path.normpath(f)))
        if not os.path.isabs(f):
            f = os.path.join(os.getcwd(), f)
        if not os.path.exists(f):
            edie('can\'t find specified file: {}'.format(f))

        relpath = os.path.relpath(f, proj_root)
        dest = os.path.join(skel_root, relpath)
        if x.args.example:
            dest = dest+'_EXAMPLE'

        print('copying: {} to {}'.format(f, dest))
        if os.path.exists(dest):
            if os.path.isdir(dest):
                shutil.rmtree(dest)
            else:
                os.remove(dest)
        if os.path.isdir(f):
            shutil.copytree(f, dest)
        else:
            os.link(f, dest)


def catchall_entry():
    DevRootParser().print_help()
    raise SystemExit(0)


def main():
    from . import _x as x

    assert x.args.action in commands

    if x.args.subaction in subcommands:
        subcommands[x.args.subaction].entry()
    else:
        catchall_entry()


commands = CommandSet([
    (['dev', 'develop', 'development'],
     DevRootParser, main, 'Modify xanity package source (if xanity-source is available).')
])

subcommands = CommandSet([
    (['copy', 'cp'], CopyParser, cmd_entry_cp, 'copy files into skeleton project.'),
])


if __name__ == "__main__":
    main()
