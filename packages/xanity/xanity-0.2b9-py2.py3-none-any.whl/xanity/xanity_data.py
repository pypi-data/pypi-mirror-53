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
import sys
import subprocess
import numpy as np
from fnmatch import fnmatch
import re
import shutil
import argparse
import pandas as pd

from .constants import *
from .common import *


#############################################################################################
class the_follwing_are_helper_functions:
    pass
################################################################################


def isa_runid(string):
    def test(string):
        return True if re.match(RUN_DIR_REGEX, os.path.split(string)[1]) else False

    if isinstance(string, str):
        return test(string)

    else:
        return all([test(s) for s in string])


def isa_rundir(dir):
    def test(string):
        return True if os.path.isdir(string) and re.match(RUN_DIR_REGEX, rundir2runid(string)) is not None else False

    if isinstance(dir, str):
        return test(dir)
    else:
        return all([test(d) for d in dir])


def split_rundir(rundir):
    def split(string):
        string = os.path.split(string)[-1]
        match = re.match(RUN_DIR_REGEX, string)
        try:
            s = match.groups()
            return s[0], s[1], int(s[2])

        except:
            return None

    if isinstance(rundir, str):
        return split(rundir)
    else:
        return [split(s) for s in rundir]


def split_runid(runid):
    def split(item):
        s = re.match(RUN_DIR_REGEX, item).groups()
        s = list(s)
        s[-1] = int(s[-1])
        return s

    if isinstance(runid, str):
        return split(runid)
    else:
        return [split(i) for i in runid]


def runid2rundir(runid):
    if isa_rundir(runid):
        return runid

    def convert(string):
        from . import _x as x

        sd = x.paths.saved_data
        rd = x.paths.run_data

        _, exp, _ = split_runid(string)
        r = os.path.join(sd, exp, string)
        if os.path.isdir(r):
            return r
        r = os.path.join(rd, exp, string)
        if os.path.isdir(r):
            return r
        else:
            return None

    if isinstance(runid, str):
        return convert(runid)
    else:
        return [convert(r) for r in runid]


def rundir2runid(path):
    def convert(string):
        return os.path.split(string)[-1]

    if isinstance(path, str):
        return convert(path)
    else:
        return [convert(p) for p in path]


def norm_run(run):
    if isinstance(run, str):
        run = [run]
    return runid2rundir(run)


def sort_runs(runs):
    if isa_rundir(runs):
        prefixes = [os.path.dirname(r) for r in runs]
        result = [(prefixes[i] + split_runid(id)) for i, id in enumerate(rundir2runid(runs))]
        result.sort(key=lambda x: x[3])
        result.sort(key=lambda x: x[2])
        result.sort(key=lambda x: x[1])

        return [os.path.join(r[0], '_'.join(r[1:-1] + (str(r[-1]),))) for r in result]

    else:

        result = split_runid(runs)
        result.sort(key=lambda x: x[2])
        result.sort(key=lambda x: x[1])
        result.sort(key=lambda x: x[0])

        return ['_'.join([r[0], r[1], str(r[2])]) for r in result]


def du(path):
    return int(subprocess.check_output([
        'du', '-bs', path
    ]).decode().split('\t')[0])


def _try_load(file):
    try:
        return pickle_load(file)
    except:
        print('problem loading {}'.format(file))
        return None


def _format_sizeof(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

#############################################################################
class The_following_are_module_level_listing_fns:
    pass
#############################################################################


def list_runnables(saved_only=False, not_saved_only=False):
    from . import _x as x

    if not saved_only and not not_saved_only:
        saved = True
        not_saved = True
    else:
        saved = saved_only
        not_saved = not_saved_only

    exps = set()

    if saved:
        for r in os.listdir(x.paths.saved_data):
            if isa_runid(r):
                exps.update(set([split_runid(r)[1]]))

    if not_saved:
        for ex in os.listdir(x.paths.run_data):
            ep = os.path.join(x.paths.run_data, ex)
            if os.path.isdir(ep) and any([isa_runid(d) for d in os.listdir(ep)]):
                exps.update(set([ex]))

    return list(exps)


def list_rundirs(experiments=None, saved_only=False, not_saved_only=False):
    from . import _x as x

    if not saved_only and not not_saved_only:
        saved = True
        not_saved = True
    else:
        saved = saved_only
        not_saved = not_saved_only

    if experiments:
        if isinstance(experiments, str):
            experiments = [experiments]
        es = list_runnables()
        experiments = [exp for exp in es if any([fnmatch.fnmatch(exp, e) for e in experiments])]

    datapaths = []

    if not_saved:
        datapaths.extend([
            os.path.join(x.paths.run_data, d)
            for d in os.listdir(x.paths.run_data) if os.path.isdir(os.path.join(x.paths.run_data, d))
        ])

    if saved:
        datapaths.extend([os.path.join(x.paths.project_root, RELATIVE_PATHS.saved_data)])

    rundirs = []
    for path in datapaths:
        for rd in [os.path.join(path, ep) for ep in os.listdir(path)]:
            if isa_rundir(rd):
                if experiments and split_rundir(rd)[1] in experiments:
                    rundirs.append(rd)
                elif not experiments or experiments is None:
                    rundirs.append(rd)

    return rundirs


def list_xanity_variables(experiment=None, path=None, runid=None):
    if not experiment and not path and not runid:
        raise ValueError('must give either an experiment or a path')

    variables = set()

    if experiment is not None:
        if isinstance(experiment, str):
            experiment = [experiment]
        for exp in experiment:
            for bd, sds, fs in os.walk(exp):
                if os.path.split(bd)[-1] == 'xanity_variables':
                    variables.update(set(tuple(item.split('.dill')[0] for item in fs if fnmatch(item, '*.dill'))))

    elif path is not None:
        for bd, sds, fs in os.walk(path):
            if os.path.split(bd)[-1] == 'xanity_variables':
                variables.update(set(tuple(item.split('.dill')[0] for item in fs if fnmatch(item, '*.dill'))))

    elif runid is not None:
        path = runid2rundir(runid)
        for bd, sds, fs in os.walk(path):
            if os.path.split(bd)[-1] == 'xanity_variables':
                variables.update(set(tuple(item.split('.dill')[0] for item in fs if fnmatch(item, '*.dill'))))

    return list(variables)


#########################################################################################
class the_following_are_for_parsing_and_selecting_subsets:
    pass
#########################################################################################


def parse_data_spec(pathstring):
    matches = set()

    if pathstring in list_runnables():
        ## an entire experiment was requested
        matches.update(list_rundirs(experiments=pathstring, include_saved=True))

    elif re.match(RUN_DIR_REGEX, pathstring):
        # a specific run was requested:
        matches.update(list_rundirs(regex=pathstring, include_saved=True))

    else:
        # a portion of a run_id was requested:
        alldata = list_rundirs()
        for item in alldata:
            if re.match(pathstring, item):
                matches.update(item)

    return list(matches)


def parse_reduce_selection(selection, requests):
    if selection is None:
        return None

    if callable(selection):
        # a single fn was given, apply everywhere:
        reduce = {selection: [vs for vs in requests.values()]}

    elif isinstance(selection, dict):
        reduce = selection
        for k, v in reduce.items():
            if isinstance(v, str):
                reduce[k] = set([v])
            else:
                reduce[k] = set(v)

    elif isinstance(selection, str):
        if hasattr(pd.DataFrame, selection):
            reduce = {getattr(pd.DataFrame, selection), '*'}

    elif isinstance(selection, (list, tuple)):
        rd = {}
        if isinstance(selection[0], (list, tuple)):
            for item in selection:
                assert len(item) == 2
                if not callable(item[0]):
                    assert callable(item[1])
                    rd.update({item[1]: item[0]})
                else:
                    assert callable(item[0])
                    rd.update({item[0]: item[1]})

        else:
            if not callable(selection[0]):
                assert callable(selection[1])
                rd.update({selection[1]: selection[0]})
            else:
                assert callable(selection[0])
                rd.update({selection[0]: selection[1]})

        reduce = rd

    return {t: f for f, ts in reduce.items() for t in ts}


def parse_data_selection(selection, experiments=None, variables=None):
    from . import _x as x

    if not selection:
        selection = {}

    elif isinstance(selection, str):
        if selection in x._runnables_avail:
            # select all variables in runnable
            selection = {selection: ''}
        else:
            # assume it's a variable
            selection = {'': selection}

    elif isinstance(selection, list):
        selection = {s: '' for s in selection if s in x._runnables_avail}

    if isinstance(selection, dict):
        for k, v in selection.items():
            if isinstance(v, str):
                selection[k] = set([v])

    if experiments:
        if isinstance(experiments, str):
            experiments = [experiments]
        for e in experiments:
            if e not in selection:
                selection[e] = ''

    if variables:
        if isinstance(variables, str):
            variables = [variables]

        if experiments:
            for v in variables:
                for e in experiments:
                    selection[e] += v
        else:
            if selection:
                for k in selection:
                    selection[k] = variables
            else:
                selection[''] = set(variables)

    dc = x.data_cache
    for k, v in selection.items():
        if k != '' and k not in dc and k not in x._runnables_avail:
            if not k in list_runnables():
                raise OSError('requested data from runnable that doesn\'t exist')

        if isinstance(v, str):
            v = [v]

        selection[k] = set(v)

        if '' in v and len(v) > 1:
            v.remove('')

    if '' in selection and len(selection.keys()) > 1:
        del selection['']

    if '' in selection:
        selection.update({e: selection[''] for e in list_runnables()})
        del selection['']

    return selection


def parse_selectors(selectors):
    kn_selectors = {
        'saved': ('saved', 'save'),
        'not_saved': ('not-saved', 'not_saved'),
        'debug': ('debug', 'debugging'),
        'not_debug': ('not-debug', 'not-debugging', 'not_debug', 'not_debugging'),
        'complete': ('complete', 'done'),
        'incomplete': ('incomplete', 'incomp', 'running'),
        'failed': ('failed', 'unsuccessful'),
        'successful': ('successful', 'succeeded', 'good', 'not-failed', 'not_failed'),
        'all': ('all',),
        'experiments': list_runnables(),
        'cache': ('cache',),
    }

    result = {}

    # if not selectors:
    #     selectors = ''

    if isinstance(selectors, str):
        selectors = selectors.split(' ')

    assert (all([isinstance(item, str) and ' ' not in item for item in selectors]))

    def is_known(string):
        for sel, aliases in kn_selectors.items():
            if string in aliases:
                return True
        return False

    for sel in selectors:
        if not is_known(sel):
            raise ValueError('didn\'t recognize selector \'{}\''.format(sel))

    for key, val in kn_selectors.items():
        if key == 'experiments':
            result[key] = [item for item in selectors if item in list_runnables()]
        else:
            result[key] = True if set(val).intersection(selectors) else False

    return result


def request_to_rundirs(selection={}, experiments=[], variables=[], all=False):
    from . import _x as x

    selection = parse_data_selection(selection, experiments, variables)

    results = []

    for e, vs in selection.items():

        rs = list_rundirs(experiments=e)

        if '' in vs:
            if all:
                results.extend(rs)
            else:
                results.append(rs[-1])
        else:
            jobs = [fetch_job(r) for r in rs]
            for v in vs:
                v_runs = []
                for j, rd in zip(jobs, rs):
                    if v in j.products:
                        v_runs.append(rd)

                if v_runs:
                    if all:
                        results.extend(v_runs)
                    else:
                        results.append(v_runs[-1])
                else:
                    if x.verbosity >1:
                        x.warn('No job in {} has produced anything matching {}. Skipping'.format(e, v))

    return results


def select_rundirs(
        experiments=None,
        saved=False, not_saved=False,
        debug=False, not_debug=False,
        complete=False, incomplete=False,
        failed=False, successful=False,
        regex=None, fnmatch_str=None,
        all=False, cache=False):  ## must accept 'cache' kwarg tho not used

    from . import _x as x

    names, rundirs, sizes, success, iscomplete, debug_flag = walk_data()

    selected = set(range(len(rundirs)))

    if not all:
        if experiments:
            selected.difference_update([i for i, val in enumerate(names)
                                        if any([fnmatch.fnmatch(val, e) for e in experiments])])

        if incomplete:
            selected.difference_update([i for i, val in enumerate(iscomplete) if val])

        if complete:
            selected.difference_update([i for i, val in enumerate(iscomplete) if not val])

        if failed:
            selected.difference_update([i for i, val in enumerate(success) if val])

        if successful:
            selected.difference_update([i for i, val in enumerate(success) if not val])

        if debug:
            selected.difference_update([i for i, val in enumerate(debug_flag) if val])

        if not_debug:
            selected.difference_update([i for i, val in enumerate(debug_flag) if not val])

        if saved:
            sp = os.path.join(x.paths.project_root, RELATIVE_PATHS.run_data)
            selected.difference_update([i for i, path in enumerate(rundirs) if sp in path])

        if not_saved:
            nsp = os.path.join(x.paths.project_root, RELATIVE_PATHS.saved_data)
            selected.difference_update([i for i, path in enumerate(rundirs) if nsp in path])

        if regex:
            selected.difference_update([i for i, path in enumerate(rundirs)
                                        if not re.match(regex, split_rundir(path)[0])])

        if fnmatch_str:
            selected.difference_update([i for i, path in enumerate(rundirs)
                                        if not fnmatch(split_rundir(path)[0], fnmatch_str)])

    return [d for i, d in enumerate(rundirs) if i in selected]


#############################################################################
class the_following_are_for_examining_data_in_the_filesystem:
    pass
#############################################################################


def scan_logs(experiment, regex, numeric=False):
    logfiles = []
    results = []
    allruns = list_rundirs(experiments=experiment)

    for root in allruns:
        if any([fnmatch(item, experiment + '_*') for item in os.listdir(root)]) and os.path.isdir(
                os.path.join(root, experiment)):
            # it's a subdir
            subdirs = [item for item in os.listdir(root) if fnmatch(item, experiment + '_*')]
            logfiles.extend([os.path.join(root, sd, experiment + DIRNAMES.EXP_LOG_SUFFIX) for sd in subdirs])
        else:
            # it's not a subdir
            logfiles.extend([os.path.join(root, experiment + DIRNAMES.EXP_LOG_SUFFIX)])

    for log in logfiles:
        if os.path.isfile(log):
            with open(log, 'r') as f:
                for line_no, line in enumerate(f.readlines()):
                    m = re.match(string=line, pattern=regex)
                    if m:
                        if numeric:
                            try:
                                results.append(np.array([float(item) for item in m.groups()]))
                            except:
                                print('could not perform numeric conversion on item in {}::{}'.format(log, line_no))
                                results.append(m.groups())
                        else:
                            results.append(m.groups())

    return results if not numeric else np.array(results, dtype='float32')


def data_info(runids=None):
    """
    Stat basic info from runs.
    :param runids:
    :return:
    """
    from . import _x as x

    cache = x.data_cache
    results = []

    if isinstance(runids, str):
        runids = [runids]
        singleton = True
    else:
        singleton = False

    for r in runids:
        try:
            d = cache[r]
            results.append(d)

        except:
            if isa_rundir(r):
                walk_data(r)
            else:
                walk_data(runid2rundir(r))

            results.append(data_info(r))

    if singleton:
        return results[0]
    else:
        return results


def walk_data(rundirs=None):
    from . import _x as x

    if rundirs is None:
        rundirs = list_rundirs()
    elif isinstance(rundirs, str):
        rundirs = [rundirs]

    ids = rundir2runid(rundirs)
    sizes = [0] * len(rundirs)
    success = [None] * len(rundirs)
    complete = [None] * len(rundirs)
    debug = [None] * len(rundirs)

    cache = x.data_cache

    for i, d in enumerate(rundirs):
        name = os.path.split(d)[-1]
        ids[i] = name

        try:
            data = cache[name]
            sizes[i] = data['size']
            success[i] = data['success']
            complete[i] = data['complete']
            debug[i] = data['debug']

        except KeyError:
            ip = os.path.join(d, 'xanity_info')

            if not os.path.isdir(d) or not re.match(RUN_DIR_REGEX, name):
                continue

            if os.path.isfile(os.path.join(ip, 'unsuccessful')):
                success[i] = False
                complete[i] = True

            elif os.path.isfile(os.path.join(ip, 'successful')):
                success[i] = True
                complete[i] = True

            elif os.path.isfile(os.path.join(ip, 'xanity_panic.dill')) \
                    or os.path.isfile(os.path.join(d, 'xanity_panic.dill')):
                success[i] = False
                complete[i] = True

            else:
                success[i] = None
                complete[i] = False

            if '-debug' in name:
                debug[i] = True
            else:
                debug[i] = False

            # get its size
            sizes[i] = du(d)

            # get its job object
            j = pickle_load(os.path.join(ip, DIRNAMES.PICKLED_JOB))

            # save it into the cache;
            cache.update({
                name: {
                    'runid': ids[i],
                    'rundir': rundirs[i],
                    'size': sizes[i],
                    'success': success[i],
                    'complete': complete[i],
                    'debug': debug[i],
                    'job': j,
                }
            })

    x.data_cache = cache
    sizes = np.array(sizes)
    success = np.array(success, dtype=bool)
    complete = np.array(complete, dtype=bool)

    return ids, rundirs, sizes, success, complete, debug


def inspect_variable(variable_name, long=False):
    locations = find_xanity_variable(variable_name)
    if locations:
        print(' {:>25}    {:<}'.format(
            'xanity variable:',
            variable_name
        ))
        print('')
        print(' {:>25}    {:<}'.format(
            'experiments:',
            len(locations)
        ))

        sizes = np.array([du(item) for item in locations])
        print(' {:>25}    {:<}'.format(
            'median size:',
            _format_sizeof(np.median(sizes))
        ))
        print(' {:>25}    {:<}'.format(
            'min, max size:',
            '{},  {}'.format(_format_sizeof(sizes.min()), _format_sizeof(sizes.max()))
        ))

        print('')
        print('  histogram of sizes:\n')
        print_histogram(sizes)


def inspect_experiment(experiment, variable_name=None, long=False, include_saved=True):
    paths = list_rundirs(experiments=experiment, include_saved=include_saved)

    print(' {:>25}    {:<}'.format(
        'experiment:',
        experiment
    ))

    print(' {:>25}    {:<}'.format(
        'total starts:',
        len(paths)
    ))

    affiliated_variables = set()
    for run in paths:
        affiliated_variables.update(set(tuple(list_xanity_variables(path=run))))

    print(' {:>25}    {:<}'.format(
        'affiliated variables:',
        str(list(affiliated_variables))
    ))

    return paths


def inspect_run(runid, variable_name=None, print_head=False, long=False, print_tail=False):
    if not isa_rundir(runid):
        # we're not inspecting a run; try environment
        return inspect_experiment(runid, variable_name=variable_name, long=long)

    try:
        runid = runid.split('-debug')[0]
        allruns = list_rundirs()
        mypath = [run for run in allruns if runid in run][0]

    except ValueError:
        print('couldn\'t find that run')
        return

    # print('looking in {}'.format(mypath))

    runlog = os.path.join(mypath, DIRNAMES.XANITY_INFO, runid + DIRNAMES.LOG_SUFFIX)
    parameters = os.path.join(mypath, DIRNAMES.SAVED_VARS, DIRNAMES.RUN_PARAMETERS)
    exps = {}

    for d in os.listdir(mypath):
        sdir = os.path.join(mypath, d)
        if os.path.isdir(sdir):
            exps.update({d: {'path': sdir, 'subexps': []}})

    for exp, ed in exps.items():
        exp_cont = os.listdir(ed['path'])
        for item in exp_cont:
            ipath = os.path.join(ed['path'], item)
            if fnmatch(item, exp + '_*') and os.path.isdir(ipath):
                ed['subexps'].append(ipath)

    print('')

    if print_head:
        if os.path.isfile(runlog):
            # print('head of runlog')
            h_rule = 0
            with open(runlog, 'r') as f:
                f.readline()
                for line in f:
                    if '##################################' in line:
                        if h_rule < 1:
                            h_rule += 1
                        else:
                            break
                    else:
                        print(line.rstrip())
        print('\n')
        return

    if print_tail:
        subprocess.call(['tail', '-n', '10', runlog])
        print('')
        return

    logfiles = [os.path.join(rroot, file) for exp, ed in exps.items() for rroot, _, files in os.walk(ed['path']) for
                file in files if fnmatch(file, '*xanity*.log')]

    varpaths = [os.path.join(rroot, ddir) for exp, ed in exps.items() for rroot, sdir, _ in os.walk(ed['path']) for ddir
                in sdir if
                fnmatch(ddir, 'xanity_variables')]

    subexp_ct = sum([len(exp['subexps']) for exp in exps.values()])

    print(' {:>25}    {:<}'.format(
        'experiments:',
        len(exps) if not subexp_ct else subexp_ct
    ))

    # print(' {:>25}    {:<}'.format(
    #     'subexperiments:',
    #     sum([ len(exp['subexps']) for exp in exps.values() ])))

    if len(logfiles) > 0:
        print(' {:>25}    {:<}'.format(
            'experiment logs:', '{}, {:^}'.format(
                len(logfiles),
                _format_sizeof(sum([du(item) for item in logfiles])),
            ))
        )

    print(' {:>25}    {:<}'.format(
        'saved xanity variables:', '{}, {:^}'.format(
            sum([len(os.listdir(pp)) for pp in varpaths]),
            _format_sizeof(sum([du(item) for item in varpaths])),
        ))
    )

    print(' {:>25}    {:<}'.format(
        '=========================', '=============')
    )

    print(' {:>25}    {:<}'.format(
        'total size:', '{}, {:^}'.format(
            len(subprocess.check_output(['find', mypath, '-type', 'f']).decode().split()),
            _format_sizeof(du(mypath))
        ))
    )

    if long:
        if os.path.isfile(parameters):
            try:
                info = pickle_load(parameters)
                print('')
                for name, val in info.items():
                    print(' {:>25}    {:<}'.format(
                        name + ':', str(val).decode())
                    )
            except:
                pass

        names = list(set([file.split('.dill')[0] for path in varpaths for file in os.listdir(path)]))
        print('')
        print(' {:>25}    {:<}'.format(
            'variable names:', names)
        )

    print('\n')


################################################################################
class the_following_are_fetchers_which_can_be_vectorized:
    pass
################################################################################


def fetch_job(rundir):
    """
    return job objects from run directories
    :param rundir:
    :return:
    """

    vectorized = False if isinstance(rundir, str) else True

    rundir = norm_run(rundir)
    jobs = []
    for rd in rundir:
        pj = os.path.join(rd, DIRNAMES.XANITY_INFO, DIRNAMES.PICKLED_JOB)
        if os.path.isfile(pj):
            try:
                jobs.append(pickle_load(pj))
            except:
                edie('found bad jobfile at {}.'.format(pj))
    return jobs if vectorized else jobs[0]


def fetch_parameter_dict(rundir):
    """
    fetch the parameter dictionary from the archive for a run or list of runs.
    :param rundir:
    :return:
    """

    vectorized = False if isinstance(rundir, str) else True
    rundir = norm_run(rundir)

    try:
        return fetch_job(rundir).parameters

    except:
        # # parse log file to get parameters
        infodir = os.path.join(rundir, DIRNAMES.XANITY_INFO)
        vardir = os.path.join(rundir, DIRNAMES.SAVED_VARS)
        pdicts = []
        param_prelude = (EXPERIMENT_LOG_HEADER.split('starting experiment')[0] + 'starting experiment').split('\n')[-1]
        run_id, expname, subexpind = split_rundir(rundir)

        def parse_headblock(file):

            pdicts = []

            with open(file, 'r') as f:
                text = ''
                foundit = False
                for line in f.readlines():
                    if not foundit:
                        if re.match(param_prelude, line):
                            foundit = True
                    else:
                        if '############' not in line:
                            text += line
                        else:
                            break

            rows = [item.split(',') for item in re.findall('.*{(.*)}.*', text)]

            for row in rows:
                pdict = {}
                for i, entry in enumerate(row):
                    opens = sum([item == '(' for item in entry])
                    closes = sum([item == ')' for item in entry])
                    if closes > opens:
                        break
                    while opens > closes:
                        entry += ',' + row[i + 1]
                        closes = sum([item == ')' for item in entry])

                    key, val = entry.split(':')
                    key = key.strip(' "\'')
                    if ',' in val:
                        ilist = []
                        for item in val.split(','):
                            item = item.strip(' [()]')
                            if item:
                                ilist.append(float(item))
                            val = tuple(ilist)
                    else:
                        val = float(val.strip(' [()]'))
                    pdict.update({key: val})

                pdicts.append(pdict)

            return pdicts

        if os.path.isfile(os.path.join(vardir, DIRNAMES.RUN_PARAMETERS)):
            pdicts = [_try_load(os.path.join(vardir, DIRNAMES.RUN_PARAMETERS))]

        if not pdicts and os.path.isfile(os.path.join(rundir, DIRNAMES.RUN_PARAMETERS)):
            pdicts = [_try_load(os.path.join(rundir, DIRNAMES.RUN_PARAMETERS))]

        # if not pdicts and metarundir and os.path.isfile(os.path.join(metarundir, DIRNAMES.RUN_PARAMETERS)):
        #     pdicts = [try_load(os.path.join(metarundir, DIRNAMES.RUN_PARAMETERS))]

        # try log files:
        if not pdicts:

            # look for per-subexperiment logfile
            files = os.listdir(rundir)

            for ff in files:
                if fnmatch(ff, '*xanity*.log'):
                    pdicts = parse_headblock(os.path.join(rundir, ff))

        # if not pdicts and metarundir:
        #
        #     # look for per-experiment logfile
        #     files = os.listdir(metarundir)
        #
        #     for ff in files:
        #         if fnmatch(ff, '*xanity*.log'):
        #             pdicts = parse_headblock(os.path.join(metarundir, ff))

        if not pdicts:

            # look for per-experiment logfile
            files = os.listdir(rundir)

            for ff in files:
                if fnmatch(ff, '*' + DIRNAMES.LOG_SUFFIX):
                    pdicts = parse_headblock(os.path.join(rundir, ff))

        if vectorized:
            return pdicts
        else:
            if pdicts:
                return pdicts[0]
            else:
                return None


def _fetch_timer_data_dict(run, timed_fn_names, reduce=None):
    """
    get a single timer_data dict from the archives
    :param run:
    :return:
    """
    vectorized = False if isinstance(run, str) else True
    rundirs = norm_run(run)
    results = []

    for r in rundirs:
        e = split_rundir(r)[1]
        j = fetch_job(r)

        if '' in timed_fn_names:
            td = j.timed_fn_results
        else:
            td = {k: j.timed_fn_results[k] for k in timed_fn_names}

        if reduce:
            for k, v in td.items():
                td[k] = reduce(td[k])

        for k, v in td.items():
            for i, vv in enumerate(v):
                record = {
                    'runid': j.runid,
                    'exp_name': j.runnable.name,
                    'call_index': i,
                    k: vv,
                }
                record.update(j.parameters)
                results.append(record)

    if vectorized:
        return results

    else:
        return results[0]


def fetch_timer_data(data_dict={}, experiments=[], names=[], reduce=None, all=False):
    """
    fetches timed_function data from the archives

    :param data_dict:
    :param experiments:
    :param names:
    :param reduce:
    :param all:
    :return:
    """
    if reduce and not callable(reduce):
        if callable(eval(reduce.strip('()'))):
            reduce = eval(reduce.strip('()'))
        else:
            raise ValueError('reduce argument should be a callable object (i.e. a function).')

    data_dict = parse_data_selection(data_dict, experiments, names)
    records = []

    for exp in data_dict:

        rundirs = request_to_rundirs({exp: data_dict[exp]}, all=all)
        records.extend(_fetch_timer_data_dict(rundirs, data_dict[exp], reduce))

    return pd.DataFrame(records)


def _fetch_variables(rundir, variables, reduce):
    from . import _x as x

    if isinstance(variables, str):
        variables = [variables]

    job = fetch_job(rundir)
    if not job:
        x.warn('couldn\'t find a jobfile at {}. Skipping.'.format(rundir))
        return None

    records = []

    for i, v in enumerate(variables):
        f = os.path.join(rundir, DIRNAMES.SAVED_VARS, v + '.dill')
        if not os.path.isfile(f):
            print('no variable in \'{}\' called \'{}\'.'.format(rundir2runid(rundir), v))
            return None

        assert job.runid == rundir2runid(rundir), 'found inconsistent job data at {}'.format(rundir)

        r = {
            'rundir': rundir,
            'job': job,
            'variable_name': v,
            'variable_value': _try_load(f),
            'variable_path': f,
        }

        if reduce is not None:
            t = [re.match(t, r['variable_name']) for t in reduce]
            if any(t):
                for mo in t:
                    fn = reduce[mo.string]
                    r['variable_value'] = fn(r['variable_value'])

        records.append(r)

        if x.verbosity > 2:
            print('fetched {}'.format(records[-1]))

    return pd.DataFrame(records)


################################################################################
class the_following_are_cache_manipulators:
    pass
################################################################################


def cache_experiment(experiment):
    """
    recreate cache for experiment
    :param experiment:
    :return:
    """

    from . import _x as x

    x.warn('(re)building xanity cache for \'{}\'.'.format(experiment))
    runs = request_to_rundirs(experiment)

    for rd in runs:

        j = fetch_job(rd)

        for v in j.products:

            if v.startswith('path://'):
                path = v.split('path://')[-1]
                if not os.path.isabs(path):
                    path = os.path.join(rd, path)
                name = os.path.split(path)[-1]
            else:
                name = v
                path = os.path.join(rd, DIRNAMES.SAVED_VARS, v + '.dill')

            if os.path.exists(path):
                register_data_obj(DataRecord(name, path, j))


def build_cache():
    """
    this (re)builds xanity's cache of data objects
    :return:
    """

    for e in list_runnables():
        cache_experiment(e)


def register_data_obj(do):
    """
    save a new piece of data into the persistent cache
    :param do:
    :return:
    """
    from . import _x as x

    c = x.data_cache

    if do.generator_name not in c:
        c[do.generator_name] = {}

    if do.generator_hash not in c[do.generator_name]:
        c[do.generator_name][do.generator_hash] = {}

    if do.param_hash not in c[do.generator_name][do.generator_hash]:
        c[do.generator_name][do.generator_hash][do.param_hash] = {}

    if do.name not in c[do.generator_name][do.generator_hash][do.param_hash]:
        c[do.generator_name][do.generator_hash][do.param_hash][do.name] = do

    else:
        # its already there:
        if c[do.generator_name][do.generator_hash][do.param_hash][do.name] != do:
            if x.verbosity > 1:
                x.log('updating data in cache')
            c[do.generator_name][do.generator_hash][do.param_hash][do.name] = do

    x.data_cache = c


################################################################################
class the_following_are_DataFrame_manipulators:
    pass
################################################################################


def _reduce_column(dataframe, reduce_fn, column_name):
    # reduce eval record data
    inds = []
    vals = []
    cts = []

    cols = dataframe.filter(regex=column_name, axis=1)
    newcols = []
    for column_name, col in cols.itercolumns:
        for index, data in col.iterrows():
            inds.append(index)
            vals.append(reduce_fn(data.values[0].flatten()))
            cts.append(len(data))

        newcols.append(pd.DataFrame(data={column_name: vals, column_name+'_pre_reduction_length':cts}))

    return pd.concat(
        [dataframe.drop(column_name, axis=1)] + newcols,
        axis=1, sort=False
    )


################################################################################
class the_following_are_implemented_as_class_methods_in_the_xanity_class :
    pass
################################################################################


def load_data(selection=None, experiments=None, variables=None, reduce=None, all=False):
    """
    loops through multiple experiment names and variable names,

    :param experiments:
    :param variables:
    :param reduce: dict of {fn:[columns],...} or list of tuples: [(column, fn),...]
    :return: a pandas Dataframe object
    """
    from . import _x as x
    reqs = parse_data_selection(selection=selection, experiments=experiments, variables=variables)
    rundirs = request_to_rundirs(selection=reqs, all=all)
    reduce = parse_reduce_selection(selection=reduce, requests=reqs)
    stack = []

    for d in rundirs:
        e = split_rundir(d)[1]
        v = reqs[e] if e in reqs else reqs['']

        data = _fetch_variables(d, v, reduce)

        if data is None:
            continue

        stack.append(data)

    if stack:
        result = pd.concat(stack, axis=0, ignore_index=True)
    else:
        result = pd.DataFrame()

    if not result.empty:
        x.register_loaded_data(result)

        parameters = pd.DataFrame([j.parameters for i, j in result['job'].iteritems()])

        variables = pd.DataFrame([{r['variable_name']: r['variable_value']} for i, r in
                                  result[['variable_name', 'variable_value']].iterrows()])

        rid = pd.DataFrame({'xanity_runid': [rundir2runid(rd) for i, rd in result['rundir'].iteritems()]})

        jobname = pd.DataFrame({'xanity_item_name': [j.runnable.name for i, j in result['job'].iteritems()]})

        return pd.concat([rid, jobname, parameters, variables], axis=1)
    else:
        return result


def timed_fn(fn):
    def wrapped(*args, **kwargs):
        from . import _x

        _x.log('[timed_fn][{}][start]'.format(fn.__name__))
        starttime = time.time()

        results = fn(*args, **kwargs)

        elapsed = time.time() - starttime
        _x.log('[timed_fn][{}][done] {} s'.format(fn.__name__, elapsed))

        td = _x.status.job.timed_fn_results
        if fn.__name__ in td:
            val = td[fn.__name__] + [elapsed]
        else:
            val = [elapsed]

        td.update({fn.__name__: val})

        return results

    return wrapped


def load_checkpoint(checkpoint_name, variables=None, overwrite=False, noload=False):
    """Try to load a pre-existing run checkpoint.
    Will return None if not found.
    """
    from . import _x as self

    if not self.args.loadcp or noload:
        warn('Checkpoint loading not enabled. Use \'--loadcp\' or \'--checkpoints\'.')
        return None

    if isinstance(variables, str):
        variables = [variables]
        solo = True
    elif variables is not None:
        solo = False



    assert isinstance(checkpoint_name, str), 'can only save one checkpoint at a time!'

    cp_dir = os.path.join(self.paths.checkpoints, self.status.job.runnable.name, checkpoint_name)
    # cp_files = [os.path.join(self.paths.checkpoints, self.status.job.runnable.name, var + '.pkl') for var in checkpoints]

    if os.path.isdir(cp_dir):

        for root, dirs, files in os.walk(cp_dir):
            if os.path.join(cp_dir, 'xanity_variables') in root:
                continue

            # s = os.path.join(cp_dir, item)
            # d = os.path.join(self.status.job.data_dir, item)

            # if os.path.isfile(s):
            #     os.link(s, d)
            # elif os.path.isdir(s):
            #     shutil.copytree(s, d, copy_function=os.link)

            for dir in dirs:
                if dir != 'xanity_variables':
                    try:
                        os.mkdir(os.path.join(self.status.job.data_dir, root.split(cp_dir)[1], dir))
                    except OSError:
                        pass

            for f in files:
                s = os.path.join(root, f)
                d = os.path.join(self.status.job.data_dir, root.split(cp_dir)[1], f)
                if os.path.isfile(d):
                    if overwrite:
                        os.remove(d)
                        os.link(s, d)
                    else:
                        pass
                else:
                    os.link(s, d)

        vardir = os.path.join(cp_dir, 'xanity_variables')

        rvars = []
        if os.path.isdir(vardir) and variables is not None:

            available = [v.split('.pkl')[0] for v in os.listdir(vardir)]

            for var in variables:
                if var not in available:
                    rvars.append(None)

                else:
                    rvars.append(pickle_load(os.path.join(vardir, var + '.pkl')))

        if rvars:
            if solo:
                return rvars[0]
            else:
                return rvars
        else:
            return True

    else:
        return [False] * len(variables) if variables is not None and not solo else False


def save_checkpoint(checkpoint_name, variables=None, cwd=True, overwrite=False):
    """
    Save some items into a named checkpoint for this experiment(/analysis).
    :param checkpoint_name:
    :param variables:
    :param cwd:
    :param overwrite:
    :return:
    """

    from . import _x as self

    if not self.args.savecp:
        # return False
        pass

    assert isinstance(checkpoint_name, str), 'can only save one checkpoint at a time!'

    cp_dir = os.path.join(self.paths.checkpoints,
                          self.status.job.runnable.name,
                          checkpoint_name)

    if variables is not None:
        variables = [variables] if not isinstance(variables, (list, tuple)) else variables
        args, kwargs = get_arg_names()
        varnames = None

        if len(args) > 1:
            varnames = args[1]
        else:
            assert 'variables' in kwargs
            varnames = kwargs['variables']
            if isinstance(varnames, str):
                varnames = [varnames]

        assert len(variables) == len(varnames)

        cp_files = [os.path.join(cp_dir,
                                 DIRNAMES.SAVED_VARS,
                                 var + '.pkl')
                    for var in varnames]

        for item, file in zip(variables, cp_files):
            if not os.path.isfile(file) or overwrite:
                if not os.path.isdir(os.path.split(file)[0]):
                    os.makedirs(os.path.split(file)[0])
                pickle_dump(item, file)

    if cwd:
        # saving runpath in file-system
        if not os.path.isdir(cp_dir):
            os.makedirs(cp_dir)

        for root, dirs, files in os.walk(self.status.job.data_dir):

            if any([os.path.split(root)[-1] in item for item in vars(DIRNAMES).values()]):
                continue

            for dir in dirs:
                if any([dir in item for item in vars(DIRNAMES).values()]):
                    continue
                try:
                    os.makedirs(os.path.join(cp_dir, root.split(self.status.job.data_dir)[1], dir))
                except OSError:
                    pass

            for f in files:
                s = os.path.join(root, f)
                d = os.path.join(cp_dir, root.split(str(self.status.job.data_dir))[1], f)

                if not os.path.isfile(d):
                    os.link(s, d)
                elif overwrite:
                    os.remove(d)
                    os.link(s, d)

        return True

    else:

        return True


def save_path(path, copy=True):
    """
    tips off xanity to the creation of a file or directory during the run.
    relative or absolute paths can be given.
    if an absolute path is given and it exists outside of the current xanity tree,
    the copy argument specifies whether it should be copied into the run-data directory or not.

    :param path:
    :return:
    """
    from . import _x as self
    if isinstance(path, str):
        path = [path]

    for p in path:
        if os.path.isabs(p) and os.path.exists(p):  # it's an absolute spec
            if self.status.job.data_dir not in p:  # path is not in this xanity run's project dir
                if copy:
                    shutil.copytree(p, os.path.join(self.status.job.data_dir, os.path.basename(p)))
    return


def save_variable(value):
    """
    internal-use: save item to current xanity-run directory without safety

    :param value:
    :param name:
    :return:
    """
    from . import _x as x
    args, kwargs = get_arg_names()
    name = kwargs['value'] if 'value' in kwargs else args[0]
    datapath = os.path.join(x.status.job.data_dir, DIRNAMES.SAVED_VARS)
    os.makedirs(datapath, exist_ok=True) if PYTHONVERSION.major == 3 else os.makedirs(datapath)
    pickle_dump(value, os.path.join(datapath, name + '.dill'))


def persistent_variable(variable):
    """
    save some local run data as stayting 'persistent' from run to run.
    :param variable:
    :param value:
    :return:
    """
    from . import _x as self

    a, k = get_arg_names()
    name = k['variable'] if 'variable' in k else a[0]
    filename = os.path.join(self.paths.persistent_data, name + '.dill')

    if not os.path.isfile(filename):
        # set if it's not already there:
        pickle_dump(variable, filename)
        return None
    else:
        # load the saved value and return it:
        variable = pickle_load(filename)
        return variable


def persistent_path(filename):
    """
    declare a file/directory to be persistent between runs of an experiment/analysis.
    :param filename:
    :return:
    """

    from . import _x as self

    name = os.path.basename(os.path.normpath(filename))

    if os.path.isabs(filename):
        s = os.path.realpath(filename)
    else:
        s = os.path.realpath(os.path.join(os.getcwd(), filename))

    d = os.path.join(self.paths.persistent_data, name)

    if not os.path.exists(filename):
        # hard-link it to persistent if it's not already there:
        shutil.copytree(s, d, copy_function=os.link)
        return None
    else:
        # hard-link it into the run-dir:
        shutil.copytree(d, s, copy_function=os.link)
        return s


################################################################################
class the_following_are_high_level_interactive_functions:
    pass
################################################################################
def summarize_data(rundirs=None, log=True, top=5, cols=2, exp_summary=True):
    from . import _x as x

    rundirs, scores, sizes, logsizes, success, complete = scan_data(
        rundirs=rundirs, sort='size', order='increasing', normalize=False, include_saved=True, include_incomplete=True)

    exps = [item for item in os.listdir(os.path.join(x.paths.project_root, 'data/runs')) if
            os.path.isdir(os.path.join(x.paths.project_root, 'data', 'runs', item))]
    datacount = len(sizes)
    top = datacount if top > datacount else top
    n_rows = int(np.ceil(float(top) / cols))
    inds_by_col = np.array_split(np.arange(top), cols)

    if datacount == 0:
        print('looks like you haven\'t created any data yet')
        return

    print('Total runs of data:     {}\n'.format(datacount))

    if exp_summary:
        print('By experiment:')
        print('\n'.join(['    {}: {}  ({} successful)'.format(
            exp,
            len(os.listdir(os.path.join(x.paths.project_root, 'data', 'runs', exp))),
            len([True for i, rd in enumerate(rundirs) if split_rundir(rd)[1] == exp and success[i]])
        ) for exp in exps]))
        print("")

    print("smallest {}:".format(top))
    for i in range(n_rows):
        rowtext = '  '
        for j, col in enumerate(inds_by_col):
            if i >= len(col):
                continue
            rowtext += '{:<35s}  {:>10s},    '.format(os.path.split(rundirs[col[i]])[-1], _format_sizeof(sizes[col[i]]))
        print(rowtext)
    print("")

    print("largest {}:".format(top))
    for i in range(n_rows):
        rowtext = '  '
        for j, col in enumerate(inds_by_col):
            if i >= len(col):
                continue
            rowtext += '{:<35s}  {:>10s},    '.format(os.path.split(rundirs[-1 - col[i]])[-1],
                                                      _format_sizeof(sizes[-1 - col[i]]))
        print(rowtext)
    print("")

    print("Log Histogram (pct of total):\n")
    print_histogram(sizes)


def scan_data(rundirs=None,
              experiments=None,
              regex=None,
              fnmatch_str=None,
              sort='alpha',
              top=0,
              order='increasing',
              normalize=False,
              include_saved=True, include_incomplete=True, include_debug=True,
              print_results=False,
              headings=20):
    if not rundirs:
        rundirs = list_rundirs(experiments=experiments,
                              include_saved=include_saved,
                              include_incomplete=include_incomplete,
                              include_debug=include_debug,
                              fnmatch_str=fnmatch_str,
                              regex=regex)

        if not rundirs:
            return [], [], [], [], [], []

    runids = rundir2runid(rundirs)
    d = data_info(runids)

    sizes = [item['size'] for item in d]
    success = [item['success'] for item in d]
    complete = [item['complete'] for item in d]
    debug = [item['debug'] for item in d]

    scores = score_info(d)
    sizes = np.array(sizes)
    logsizes = np.log(sizes)
    success = np.array(success, dtype=bool)
    complete = np.array(complete, dtype=bool)

    # corrections
    # scores = scores-scores.min()

    n_scores = 100 * scores / np.median(scores)
    n_sizes = 100 * sizes / np.median(sizes)
    n_logsizes = 100 * logsizes / np.median(logsizes)

    composite_scores = n_scores + n_logsizes
    n_composite_scores = 100 * composite_scores / np.median(composite_scores)

    if normalize:
        scores = n_scores
        sizes = n_sizes
        logsizes = n_logsizes
        composite_scores = n_composite_scores

    if sort == 'composite_score':
        ranks = np.argsort(composite_scores)
    elif sort == 'alpha':
        ranks = np.argsort(runids)
    elif sort == 'size':
        ranks = np.argsort(sizes)
    elif sort == 'score':
        ranks = np.argsort(scores)
    else:
        raise ValueError("I didn't understand that sorting request")

    if sort:
        if order in ['decreasing', 'descending']:
            ranks = ranks[::-1]
        elif order in ['increasing', 'ascending']:
            pass
        else:
            raise ValueError("didn't recognize that sort order request")

    if isinstance(top, int) and top > 0:
        ranks = ranks[:top]

    if print_results:

        for i, index in enumerate(ranks):
            if headings and headings > 0 and not i % headings:
                print("#############################################################################################")
                print("#            run                                score     size      logsize    composite    #")
                print("#############################################################################################")
                #   2019-03-05-202910_experiment1_73        0.22      0.2 %      0.2 %      0.4 %

            if not normalize:
                print("   {:40s}    {:5.1f}    {:8s}    {:5.1f}    {:5.1f} %".format(
                    runids[index], scores[index], _format_sizeof(sizes[index]), logsizes[index], composite_scores[index]
                ))
            else:
                print("   {:40s}    {:5.1f} %    {:5.1f} %    {:5.1f} %    {:5.1f} %".format(
                    runids[index], scores[index], sizes[index], logsizes[index], composite_scores[index]
                ))

    return [rundirs[i] for i in ranks], scores[ranks], sizes[ranks], logsizes[ranks], success[ranks], complete[ranks]


def score_run(run):
    """
        Calculate a heuristic score for imporance of individual runs of experiments

        :param run:
        :return:
        """

    if isinstance(run, str):
        run = [run]

    if isa_runid(run):
        run = runid2rundir(run)

    info = data_info(run)
    return score_info(info)


def score_info(runinfo):
    """
    given a list of run information, score it
    :param runinfo:
    :return:
    """
    scores = np.zeros(len(runinfo))

    for i, r in enumerate(runinfo):

        if 'debug' not in r['runid']:
            scores[i] += 1

        # look at the top-level structure
        c1 = os.listdir(r['rundir'])
        scores[i] += len(c1) - 2  # two dirs created by xanity

        # points for files in 'saved_variables'
        for sd, dirs, fs in os.walk(r['rundir']):

            if sd.endswith(DIRNAMES.SAVED_VARS):
                for _ in fs:
                    scores[i] += 1

            for ff in fs:
                # point for log and another if it's big
                if ff.endswith(DIRNAMES.LOG_SUFFIX):
                    scores[i] += 1
                    if os.stat(os.path.join(sd, ff)).st_size > 1000:
                        scores[i] += 1

    return scores


def print_histogram(values, height=10, width=74, barwidth=2, ticks=4, log=True):
    if not isinstance(values, np.ndarray):
        values = np.array(values)
    values = values.ravel()

    bins = int(width / barwidth)
    tick_inds = list((np.arange(ticks).astype(float) / np.array((ticks - 1)).astype(float) * bins).astype(int))
    tick_space = int(width / (ticks + 1))

    hist, edges = np.histogram(values, bins=bins, density=True)
    if log:
        hist, _ = np.histogram(np.log(values), bins=bins, density=True)

    hist = (height * hist.astype(float) / hist.max().astype(float)).astype(int)

    histarray = []

    for i, col in enumerate(hist):
        histarray.append(np.concatenate([
            np.zeros(height - hist[i]),
            np.ones(hist[i] + 1)
        ]))

    for i, row in enumerate(np.stack(histarray).T):
        print('  {}'.format(''.join([''.join(['#'] * barwidth) if x else ''.join([' '] * barwidth) for x in row])))

    print(''.join([" "] * (tick_space)).join(['{:8s}'.format(_format_sizeof(entry)) for entry in edges[tick_inds]]))
    print('\n')


def purge(experiments, **kwargs):
    from . import _x as x

    if 'cache' in kwargs and kwargs['cache']:
        x.close()
        shutil.rmtree(x.paths.cache)
        die('cleared xanity caches')

    if experiments == 'all' or 'all' in kwargs and kwargs['all']:
        experiments = list_runnables()

    elif isinstance(experiments, str):
        experiments = [experiments]

    for experiment in experiments:
        dirs = inspect_experiment(experiment, long=True, include_saved=False)
        if dirs:
            try:
                if not confirm('You are about to delete all data associated with \'{}\'.\n'
                               'are you sure about that??'.format(experiment),
                               default_response=False):
                    return
            except KeyboardInterrupt:
                print('')
                return

            for path in dirs:
                shutil.rmtree(path)
            # remove_broken_links()


def prune(rundirs=None,
          metric='size', threshold=0.01, unit='fraction',
          print_sizes=False, human_readable=False,
          full_path=False, full_path_only=False, count_only=False,
          delete=False, include_saved=False,
          print_scores=False):
    acceptable_metrics = ['size', 'logsize', 'score', 'composite_score']
    acceptable_units = ['percent', 'unit', 'fraction', 'bytes', 'B', 'b', 'bits', 'byte', 'bit']

    if unit in ['B', 'bytes']:
        unit = 'bytes'
    elif unit in ['b', 'bits']:
        unit = 'bits'

    if isinstance(threshold, str):

        if 'b' in threshold:
            unit = 'bits'
            threshold = threshold.rstrip('b')

            if 'k' in threshold.lower():
                threshold = float(threshold.lower().split('k')[0]) * (10 ** 3)
            elif 'm' in threshold.lower():
                threshold = float(threshold.lower().split('m')[0]) * (10 ** 6)
            elif 'g' in threshold.lower():
                threshold = float(threshold.lower().split('g')[0]) * (10 ** 9)
            elif 't' in threshold.lower():
                threshold = float(threshold.lower().split('t')[0]) * (10 ** 12)

        elif 'B' in threshold:
            unit = 'bytes'
            threshold = threshold.rstrip('B')

            if 'k' in threshold.lower():
                threshold = float(threshold.lower().split('k')[0]) * (2 ** 10)
            elif 'm' in threshold.lower():
                threshold = float(threshold.lower().split('m')[0]) * (2 ** 20)
            elif 'g' in threshold.lower():
                threshold = float(threshold.lower().split('g')[0]) * (2 ** 30)
            elif 't' in threshold.lower():
                threshold = float(threshold.lower().split('t')[0]) * (2 ** 40)

        elif '%' in threshold:
            unit = 'percent'
            threshold = float(threshold.strip('%'))

        elif '/' in threshold:
            unit = 'fraction'
            threshold = float(threshold.split('/')[0]) / float(threshold.split('/')[1])

        elif '.' in threshold:
            if not unit:
                unit = 'fraction'
            threshold = float(threshold)

        else:
            if not unit:
                unit = 'bytes'
            threshold = int(threshold)

    if not isinstance(threshold, (int, float)):
        print('must specify threshold as a scalar quantity')
        return
    if not isinstance(metric, str) or metric not in acceptable_metrics:
        print('must specify metric ({})'.format(acceptable_metrics))
        return
    if not isinstance(unit, str) or unit not in acceptable_units:
        print('must specify unit ({})'.format(acceptable_units))
        return

    rundirs, scores, sizes, logsizes, success, complete = scan_data(
        rundirs=rundirs,
        sort='size', order='ascending', normalize=False,
        include_saved=include_saved)

    if metric == 'size':
        prunescores = sizes
    elif metric == 'logsize':
        prunescores = logsizes
    elif metric == 'score':
        prunescores = scores
    elif metric == 'logscore':
        prunescores = np.log(scores)

    if unit == 'percent':
        prunescores = prunescores.astype(float) / np.max(prunescores) * 100.0
    elif unit == 'fraction':
        prunescores = prunescores.astype(float) / np.max(prunescores)
    elif unit == 'bits':
        prunescores = 8 * sizes

    del_upto = np.searchsorted(prunescores, threshold, side='left')

    if count_only:
        print('these params would prune {} runs out of {}'.format(del_upto, len(scores)))
        return del_upto

    if delete:
        try:
            if not confirm('you are about to delete {} runs worth of precious data. are you sure?'.format(del_upto),
                           default_response=False):
                return
        except KeyboardInterrupt:
            print('')
            return

        rmfailpaths = []

        def log_failed_dirs(function, path, excinfo):
            rmfailpaths.append(path)

        for path in rundirs[:del_upto]:
            shutil.rmtree(path, ignore_errors=False, onerror=log_failed_dirs)
            if path not in rmfailpaths:
                print('removed {}'.format(path))

    else:
        col = []
        if full_path or full_path_only:
            col.append(rundirs[:del_upto])
        else:
            col.append([row.split(os.sep)[-1] for row in rundirs[:del_upto]])

        print('## threshold = {} {}'.format(threshold, '%' if unit == 'fraction' else unit))

        if print_sizes and not full_path_only:
            if human_readable:
                col.append([_format_sizeof(row) for row in sizes[:del_upto]])
            else:
                col.append([row for row in sizes[:del_upto]])

        if print_scores:
            if unit == 'percent':
                col.append(['{:5.1f}%'.format(row) for row in prunescores[:del_upto]])
            else:
                col.append(['{:5.1g}'.format(row) for row in prunescores[:del_upto]])
        for row in zip(*col):
            print(' '.join(['{:<}'] * len(col)).format(*row))


# ###############################################
# Main, module-level, parser:
class DataRootParser(argparse.ArgumentParser):
    def __init__(self):
        from . import _root_parser
        super(DataRootParser, self).__init__(prog='xanity-data',
                                             description='interact with xanity project data',
                                             parents=[_root_parser],
                                             add_help=False)
        self.add_argument('subaction')

    def parse_known_args(self, *args, **kwargs):
        kn, unk = super(DataRootParser, self).parse_known_args(*args, **kwargs)

        if kn.subaction in subcommands:
            return subcommands[kn.subaction].parser().parse_known_args()
        else:
            return kn, unk


# Subordinate Parsers:

class ScoreParser(argparse.ArgumentParser):
    def __init__(self):
        super(ScoreParser, self).__init__(prog='xanity-data score',
                                          description='score relative importance of runs',
                                          parents=[DataRootParser()])
        self.add_argument('selectors', nargs='*', type=str)
        self.add_argument('--composite', '-C', action='store_true', help='sort by a composite of score and size')
        self.add_argument('--size', '-s', action='store_true', help='sort by size')
        self.add_argument('--score', '-S', help='sort by score')
        self.add_argument('--headings', '-H', action='store', type=int, default=20)
        self.add_argument('--normalize', '-n', action='store_true')
        # self.add_argument('--logarithmic','-L', action='store_true', default=True)
        self.add_argument('--ascending', '-a', action='store_true')
        self.add_argument('--descending', '-d', action='store_true')
        self.add_argument('--top', '-t', default=0)
        self.add_argument('--name', '-N', action='store_true')
        self.add_argument('--alpha', action='store_true')


class SummarizeParser(argparse.ArgumentParser):
    def __init__(self):
        super(SummarizeParser, self).__init__(prog='xanity-data summarize',
                                              description='summarize data',
                                              parents=[DataRootParser()])
        self.add_argument('selectors', nargs='*', type=str)
        self.add_argument('--top', '-t', type=int, default=4)
        self.add_argument('--columns', '-c', type=int, default=2)


class PruneParser(argparse.ArgumentParser):
    def __init__(self):
        super(PruneParser, self).__init__(prog='xanity-data prune',
                                          description='prune data from project',
                                          parents=[DataRootParser()])
        self.add_argument('selectors', nargs='*', default=['all'])
        self.add_argument('--threshold', '-t', type=str, default='0.001')
        self.add_argument('--metric', '-m', type=str, default='size')
        self.add_argument('--unit', '-u', type=str)
        self.add_argument('--human-readable', '-H', action='store_true')
        self.add_argument('--path', '-p', action='store_true')
        self.add_argument('--full-path-only', '-P', action='store_true')
        self.add_argument('--delete', '-D', action='store_true')
        self.add_argument('--count-only', '-c', action='store_true')
        self.add_argument('--saved', action='store_true')
        self.add_argument('--scores', '-s', action='store_true')


class InspectParser(argparse.ArgumentParser):
    def __init__(self):
        super(InspectParser, self).__init__(prog='xanity-data inspect',
                                            description='inspect xanity data',
                                            parents=[DataRootParser()])
        self.add_argument('selectors', nargs='*', default=['all'])
        self.add_argument('--long', '-l', action='store_true', help='prints variable names')
        self.add_argument('--log', '-L', action='store_true', help='prints head of root log')
        self.add_argument('--end', '-E', action='store_true', help='prints tail of root log')
        #self.add_argument('--variable', '-v', action='store_true', help='indicates that the arg is a variable')
        #self.add_argument('--experiment', '-e', action='store_true', help='indicates that the arg is a variable')


class PurgeParser(argparse.ArgumentParser):
    def __init__(self):
        super(PurgeParser, self).__init__(prog='xanity-data purge',
                                          description='purge data from project',
                                          parents=[DataRootParser()])
        self.add_argument('selectors', nargs='*', type=str)


class ListParser(argparse.ArgumentParser):
    def __init__(self):
        super(ListParser, self).__init__(prog='xanity-data list',
                                         description='list xanity data',
                                         parents=[DataRootParser()])
        self.add_argument('selectors', nargs='*', help='complete, incomplete, failed, successful')
        self.add_argument('--count-only', '-c', action='store_true', help='print only the count')


# ##################################
# Subordinate entry-points :
def cmd_entry_score():
    from . import _x as x

    if 'help' in x.args.selectors:
        ScoreParser().print_help()
        raise SystemExit(0)

    if x.args.composite:
        sort = 'composite_score'
    elif x.args.size:
        sort = 'size'
    elif x.args.score:
        sort = 'score'
    elif x.args.alpha or x.args.name:
        sort = 'alpha'
    else:
        sort = 'size'

    if x.args.ascending and not x.args.descending:
        order = 'ascending'
    elif x.args.descending and not x.args.ascending:
        order = 'ascending'
    elif not x.args.descending and not x.args.ascending:
        order = 'descending'
    else:
        raise ValueError('conflicting order requests,')

    dirs = select_rundirs(**parse_selectors(x.args.selectors))
    if dirs:
        scan_data(rundirs=dirs, print_results=True, sort=sort, order=order, top=x.args.top, headings=x.args.headings,
                  normalize=x.args.normalize)


def cmd_entry_summarize():
    from . import _x as x

    if 'help' in x.args.selectors:
        SummarizeParser().print_help()
        raise SystemExit(0)

    dirs = select_rundirs(**parse_selectors(x.args.selectors))
    if dirs:
        summarize_data(rundirs=dirs, top=x.args.top, cols=x.args.columns, exp_summary=not x.args.selectors)


def cmd_entry_prune():
    from . import _x as x

    if 'help' in x.args.selectors:
        PruneParser().print_help()
        raise SystemExit(0)

    dirs = select_rundirs(**parse_selectors(x.args.selectors))
    if dirs:
        prune(rundirs=dirs, threshold=x.args.threshold, metric=x.args.metric, unit=x.args.unit,
              human_readable=x.args.human_readable, full_path=x.args.path,
              full_path_only=x.args.full_path_only, delete=x.args.delete, count_only=x.args.count_only,
              include_saved=x.args.saved, print_scores=x.args.scores)


def cmd_entry_inspect():
    from . import _x as x

    if 'help' in x.args.selectors:
        InspectParser().print_help()
        raise SystemExit(0)

    raise NotImplemented


def cmd_entry_purge():
    from . import _x as x

    if 'help' in x.args.selectors:
        PurgeParser().print_help()
        raise SystemExit(0)

    purge(**parse_selectors(x.args.selectors))


def cmd_entry_list():
    from . import _x as x

    if 'help' in x.args.selectors:
        ListParser().print_help()
        raise SystemExit(0)

    if not x.args.selectors:
        x.args.selectors = ['all']
    selection = parse_selectors(x.args.selectors)
    dirs = select_rundirs(**selection)
    if dirs:
        if x.args.count_only:
            print(len(dirs))
        else:
            print('\n'.join(dirs))


def cmd_entry_catchall():
    edie(_cli_generate_help_text())


def _cli_generate_help_text():
    text = " xanity data action [--help|-h]\n\n" \
           "   xanity-data invoked without specifying an action. Available actions include: \n\n" \
           "{}".format(
                '\n'.join(['   {} [--help]'.format('|'.join(item.aliases)) for item in subcommands])
            )
    return text


def _generate_help_text():
    text = "available commands include:\n"

    for item in vars(commands).values():
        aliases = list(item.aliases)[1:]
        if len(aliases) > 1:
            if len(aliases) > 3:
                aliases = aliases[:3]
            text += "    {:<7}{:<25} {:}\n".format(item.name, '['+'|'.join(aliases) + ']', item.description)
        else:
            text += "    {:<7}{:<25} {:}\n".format(item.name, '', item.description)

    return text


def main():
    from . import _commands
    from . import _x as x

    assert x.args.action == _commands.data

    if x.args.subaction == 'help':
        DataRootParser().print_help()
        raise SystemExit(0)

    if x.args.subaction in subcommands:
        subcommands[x.args.subaction].entry()

    else:
        cmd_entry_catchall()


commands = CommandSet([
    # ([ aliases ], parser-type, entry-fn, description )
    (['data'], DataRootParser, main, 'interact with project data'),
])


# Define commands:
subcommands = CommandSet([
    # ([ aliases ], parser, entry-fn, description )
    (['prune'], PruneParser, cmd_entry_prune, 'prune data-items from project'),
    (['score', 'scores', 'scan'], ScoreParser, cmd_entry_score, 'heuristically score relevance of data-items'),
    (['summarize', 'summary'], SummarizeParser, cmd_entry_summarize, 'summarize data-items in project'),
    (['inspect'], InspectParser, cmd_entry_inspect, 'inspect data-items'),
    (['purge'], PurgeParser, cmd_entry_purge, 'purge data-items'),
    (['list'], ListParser, cmd_entry_list, 'list data-items'),
])


if __name__ == '__main__':
    main()
