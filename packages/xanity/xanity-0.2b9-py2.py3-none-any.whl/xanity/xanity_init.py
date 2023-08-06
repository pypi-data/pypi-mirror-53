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

import os
import os.path as path
import shutil
import pkg_resources
import subprocess
import argparse
import shlex

from .common import confirm, find_xanity_root, die, edie, CommandSet

skel_root = pkg_resources.resource_filename(__name__, 'skeleton')

exclude_list = [
    "__pycache__",
    "*~",
    ".*~",
]


class InitParser(argparse.ArgumentParser):
    def __init__(self):
        from . import _root_parser
        super(InitParser, self).__init__(prog='xanity-init',
                                         description='Make a directory into a xanity project.'
                                                     'Existing files will not overwritten.',
                                         parents=[_root_parser])
        self.add_argument('directory', nargs='?', help='path to location of new or existing xanity project')
        self.add_argument('--examples', '--with-examples', action='store_true',
                          help='include example experiments and analyses')


def initialize(project_root, include_examples=False):
    if os.path.isdir(os.path.join(project_root, '.xanity')):
        if not confirm('Init over existing xanity project?', default_response=False):
            die('')

    if not include_examples:
        exclude_list.extend([r'"*_EXAMPLE"'])

    rsync_cmd = ['rsync', '-r', '--ignore-existing', skel_root + os.sep, project_root + os.sep]
    rsync_cmd.extend(['--exclude={}'.format(item) for item in exclude_list])

    if include_examples:
        print('Initializing xanity project directory with examples: {}'.format(project_root))
    else:
        print('Initializing xanity project directory: {}'.format(project_root))

    subprocess.call(rsync_cmd)

    # walk tree and rename _EXAMPLE files or delete them
    def handle_examples():
        for base, dirs, files in os.walk(project_root):
            for item in dirs + files:

                if item.endswith('_EXAMPLE'):

                    installed = os.path.join(base, item.split('_EXAMPLE')[0])
                    example = os.path.join(base, item)

                    if item in files:
                        try:
                            if include_examples:
                                try:
                                    os.remove(installed)
                                except OSError:
                                    pass
                                os.rename(example, installed)
                            else:
                                os.remove(example)
                        except OSError:
                            pass

                    elif item in dirs:
                        try:
                            if include_examples:
                                try:
                                    shutil.rmtree(installed)
                                except OSError:
                                    pass
                                os.rename(example, installed)
                            else:
                                shutil.rmtree(example)
                        except OSError:
                            pass
                        handle_examples()
                        return

    handle_examples()


def git_subroutine(project_root):
    # print(
    #     "#####################################\n"
    #     "##               git               ##\n"
    #     "#####################################\n"
    # )

    gi_pak = path.join(project_root, '.gitignore-deploy')
    gi_exist = path.join(project_root, '.gitignore')

    if path.isfile(gi_exist):
        print('found existing .gitignore. NOT clobbering it')
        if path.isfile(gi_pak):
            os.remove(gi_pak)

    #        # check ages
    #        gi_pak_age = os.stat(gi_pak).st_mtime
    #        gi_exist_age =  os.stat(gi_exist).st_mtime
    #    
    #        # overwrite existing
    #        os.remove(gi_exist)
    #            
    else:
        os.rename(gi_pak, gi_exist)
        print('deployed xanity\'s .gitignore')

    # initialize a git repo
    if subprocess.call(
            shlex.split('bash -lc  \'type -t git\''),
            stdout=open('/dev/null', 'w'),
            stderr=subprocess.STDOUT):
        print('could not find a git installation')
        return None

    else:
        # git is working
        print('checking whether a repo exists...')
        if not subprocess.call(
                shlex.split('git status'),
                stdout=open('/dev/null', 'w'),
                stderr=subprocess.STDOUT):
            # it is a git repo already
            print('leaving existing Git repo alone.')
        else:
            try:
                result = subprocess.check_output(['git', 'init', project_root], stderr=subprocess.STDOUT)
                print("successfully created a new git repo.")
            except subprocess.CalledProcessError as e:
                print("error during creation of new git repo.")
                print(e.output.replace('\n', '\n[git output]  '))
                raise SystemExit(e.returncode)

            if 'Reinitialized existing Git repository' not in result.decode():
                # nothing went wrong

                try:
                    subprocess.check_call(['git', 'add', '-A'])
                    # print('\nmade an initial commit to your new repo')
                except Exception:
                    print("xanity was unable to add files to git")
                    raise SystemExit

                try:
                    subprocess.check_call(['git', 'commit', '-am', 'xanity initial commit'],
                                          stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
                    print('Files committed to new git repo. Use \'git status\' to see what\'s up\n')
                except Exception:
                    print("xanity was unable to commit to the new git repo")
                    raise SystemExit

            else:
                print("xanity may have accidentally reset your git repo. "
                      "Try git ref-log and the web for help :P. sorry.")
                raise SystemExit


def main():
    from . import _x as x
    from . import _commands
    from . import _root_parser

    assert x.args.action == _commands.init

    if x.args.directory and 'help' in x.args.directory:
        InitParser().print_help()
        raise SystemExit(0)

    if x.args.directory:
        dirspec = x.args.directory
    else:
        dirspec = ''

    if not dirspec:
        x_root = find_xanity_root()
        dirspec = str(os.getcwd()) if not x_root else x_root

    dirspec = path.expandvars(path.expanduser(dirspec))

    if os.path.isdir(dirspec):
        project_root = os.path.abspath(dirspec)
        # print('Initializing xanity inside existing directory: {}'.format(project_root))

    else:
        project_root = os.path.abspath(os.path.join(os.getcwd(), dirspec))

    initialize(project_root, x.args.examples)
    opwd = os.getcwd()
    os.chdir(project_root)
    git_subroutine(project_root)
    os.chdir(opwd)


commands = CommandSet([
    # ([ aliases ], parser-type, entry-fn, description )
    (['init', 'initialize'], InitParser, main, 'make a directory into a xanity project.'),
])


if __name__ == "__main__":
    main()
