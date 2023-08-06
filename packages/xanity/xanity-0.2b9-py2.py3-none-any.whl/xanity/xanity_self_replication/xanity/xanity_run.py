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

import argparse
from .common import CommandSet


class RunParser(argparse.ArgumentParser):
    def __init__(self):
        from . import _root_parser
        super(RunParser, self).__init__(prog='xanity-run',
                                        description='run xanity experiments and analyses',
                                        parents=[_root_parser])
        self.add_argument('items', nargs='*',
                          help='specify the experiments and analyses to run')
        self.add_argument('--initialize', action='store_true', help='run xanity init before experiments')
        self.add_argument('--setup', action='store_true', help='run xanity setup before experiments')
        self.add_argument('-p', '--parameter', action='append')
        # self.add_argument('-a', '--and-analyze', action='store',
        #                   help="request that data be analyzed upon completion of experiment")
        self.add_argument('--loadcp', action='store_true',
                          help='request experiment look for and load stored checkpoints from src/include/persistent'
                               ' rather than start from scratch')
        self.add_argument('--savecp', action='store_true',
                          help='request experiment try to save checkpoints to src/include/persistent'
                               ' (will NOT overwrite)')
        self.add_argument('--checkpoints', action='store_true')
        self.add_argument('--count', '-c', type=int, default=1, help="will run the experiment(s) multiple times")
        self.add_argument('--runid', '-i', action='store', help="(used with analyze only) specific run-id to analyze")
        self.add_argument('--profile', action='store_true', help='run cProfile attached to each experiment')
        self.add_argument('--force', '-f', action='store_true', help="force xanity to ignore re-usable "
                                                                     "data and run again.")


def main():
    from . import new_xanity_session
    from . import _commands
    from . import _x as x

    assert x.args.action == _commands.run

    if not hasattr(x.args, 'count'):
        n_runs = 1
    else:
        n_runs = x.args.count

    for run_idx in range(n_runs):
        from . import _x as x
        x.internal_run()
        if run_idx < n_runs-1:
            new_xanity_session()
    return


commands = CommandSet([
    # ([ aliases ], parser-type, entry-fn, description )
    (['run'], RunParser, main, 'run experiments/analyses'),
])


if __name__ == '__main__':
    main()
