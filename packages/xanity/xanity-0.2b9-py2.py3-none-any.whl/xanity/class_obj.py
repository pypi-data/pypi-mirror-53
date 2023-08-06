import logging
import tarfile
import shutil
import datetime
import profile
import gc

from sys import version_info as PYTHONVERSION
if PYTHONVERSION.major == 2:
    from codecs import open

elif PYTHONVERSION.major == 3:
    pass

from itertools import product

from .common import *
from .constants import *


class XanityClass(object):

    def __init__(self):

        self.act_tags = ContextStack()

        with self.act_tags(ACTIVITIES.CONSTRUCT):
            self._start_time = time.localtime()
            self.run_id = time.strftime('%Y-%m-%d-%H%M%S', self._start_time)
            self.project_name = None
            self.paths = None
            self.action = None
            self.args = None
            self.unknownargs = None
            self.debug = False
            self.debug_xanity = False
            self.verbosity = 1
            self.timed_fn_results = {}
            self.status = Status()

            self._importers = set()
            self._invoker = None
            self._data_deps = {}
            self._paramset_reqs = {}
            self._trial_reqs = {}
            self._invocation = None
            self._runnables_avail = RunnableList()
            self._runnable_reqs = RunnableList()
            self._run_q = JobList()
            self._live_modules = {}
            self._profile = False
            self._requests_resolved = False
            self._has_run = False
            self.__cache = None
            self._data_scan_results = None

            # order here is very particular!
            self._init_logger()
            self._resolve_xanity_root()
            self._parse_args()
            self._init_cache()

            if self.debug:
                self.run_id += '-debug'

    def _init_cache(self):
        """
        initializes xanity's cache (a \'shelve\' object).
        :return:
        """
        from .xanity_env import check_environment

        if self.__cache is None and self.paths is not None:
            if check_environment(self.paths.conda_env):  # don't mess with cache from inside other python interpreters !!!
                if not os.path.exists(self.paths.cache_index):
                    # will have to make a cache.  check parent directory
                    cr = os.path.sep.join(os.path.split(self.paths.cache_index)[:-1])
                    if not os.path.exists(cr):
                        os.makedirs(cr)
                self.__cache = Cache(str(self.paths.cache_index))

    @property
    def data_cache(self):
        """
        access method for cache
        :return:
        """
        from pickle import UnpicklingError

        try:
            if 'data' not in self.__cache:
                self.__cache['data'] = {}
            return self.__cache['data']

        except UnpicklingError:
            self.close()
            shutil.rmtree(self.paths.cache)
            self._init_cache()
            self.__cache['data'] = {}
            return self.__cache['data']

    @data_cache.setter
    def data_cache(self, dict):
        c = self.__cache['data']
        c.update(dict)
        self.__cache['data'] = c

    def _absolute_trigger(self):
        """
        this is called to start any runnables
        :return:
        """
        with self.act_tags(ACTIVITIES.RUN):

            # correct_environment() ### this should already have been done!
            self._parse_runnables()
            self._resolve_requests()
            self._process_parameters()

            # for r in self._runnables_avail.values():
            #     self._cache.store_object(r.module_path, r.filehash, r, r.module_path)

            self._run_basic_prelude()

            try:
                if self._run_q.experiments:
                    self._run_all_exps()
                if self._run_q.analyses:
                    self._run_all_anals()

            except (KeyboardInterrupt, BdbQuit) as e:
                self.log('xanity terminated by user.')
                die('xanity terminated by user.')

            self._has_run = True
        return

    def close(self):
        if self.__cache is not None:
            try:
                self.__cache.close()
                self.__cache = None
            except:
                pass

    def __del__(self):
        self.close()

    def _parse_args(self, args=None):
        """ parse MODULE arguments """

        from . import _commands, _root_parser

        if self._invocation == INVOCATION.HOOK:

            # here we have to build up some kind of command line arg string
            if args and isinstance(args, str):
                args = args.split(' ')
            elif args is None:
                args = []

            if self._invoker in [exp.module_path for exp in self._runnables_avail.experiments.values()]:
                args.extend([_commands.run.name, file2mod(self._invoker)])

            elif self._invoker in [anal.module_path for anal in self._analyses_avail.values()]:
                args.extend([_commands.analyze.name, '-a', file2mod(self._invoker)])

            args.extend(sys.argv[1:])  # pickup any commandline args

        elif self._invocation == INVOCATION.COMMAND:
            if args and isinstance(args, str):
                args = args.split(' ')
            elif args is None:
                args = []

        self.args, self.unknownargs = _root_parser.parse_known_args(args=args)

        if isinstance(self.args.verbosity, int):
            self.verbosity = self.args.verbosity
        elif isinstance(self.args.verbosity, str):
            self.verbosity = self.args.verbosity.count('v') + 1

        self.debug = self.args.debug
        self.debug_xanity = self.args.debug_xanity

        if self.debug_xanity and self.verbosity < 3:
            self.verbosity = 3

        if self.args.action in _commands.run:
            self._profile = self.args.profile
            self._force = self.args.force

            if self.args.checkpoints:
                self._savecp = True
                self._loadcp = True
            else:
                self._savecp = self.args.savecp
                self._loadcp = self.args.loadcp

        elif self.args.action not in _commands and self.args.action in dir(self):
            self.action = getattr(self, self.args.action)

        # elif self.args.action not in _commands:
        #     # # can\'t use edie for import safety
        #     print('xanity doesn\'t recognize that command. Try: \'xanity --help\'.', file=sys.stderr)
        #     raise SystemExit(os.EX_USAGE)
        #
        # elif self.unknownargs:
        #     # # can\'t use edie for import safety
        #     print(
        #         'xanity doesn\'t recognize that command. Try: \'xanity {} --help\'.'.format(self.args.action),
        #         file=sys.stderr)
        #     raise SystemExit(os.EX_USAGE)

        self.action = self.args.action

    def _parse_runnables(self):
        """
        docstring
        :return:
        """

        exp_list = self.list_avail_experiments()
        anal_list = self.list_avail_analyses()

        # # warn if any experiments and analyses share a name
        if any([en == an for en, ep in exp_list for an, ap in anal_list]):
            edie('found an analysis with the same name as an experiment. Please change one to something unique.')

        for name, fullpath in exp_list:
            self._runnables_avail.update({name: Experiment(fullpath)})

        for name, fullpath in anal_list:
            self._runnables_avail.update({name: Analysis(fullpath)})

    def _resolve_requests(self):
        """
        parse requested action_objects and options

        The strategy is to add everything first, assuming they can all be run.
        The modules won't be loaded until 'just in time', so we won't know what's
        possible until then.  After the modules are loaded and associations registered,
        we can purge what's impossible

        """

        from pyparsing import nestedExpr as NestedExpr

        # define things user wants to run
        if self.args.items:
            expreqd = [os.path.split(item)[-1].split('.py')[0] for item in self.args.items]

            if self.verbosity > 1:
                print('looking for requested runnables: {}'.format(expreqd))

            if not all([item in self._runnables_avail for item in expreqd]):
                print('couldn\'t find a requested experiment.')
                raise SystemExit(1)

            self._runnable_reqs = {item: self._runnables_avail[item] for item in expreqd}

        else:
            if self._invocation == INVOCATION.HOOK:
                name = os.path.split(self._invoker)[-1].split('.py')
                self._runnable_reqs.update({name: self._runnables_avail[name]})

            else:
                # do a master run !
                self.warn('!!!! running the entire project !!!!')
                self._runnable_reqs = self._runnables_avail

        # # pickup parameter requests from the command-line
        if 'parameter' in self.args and self.args.parameter is not None and len(self.args.parameter) > 0:
            pdict = {}

            def seq_dive(item):
                # item should be either list or str

                if isinstance(item, str):

                    # could be number
                    if item.isdigit():
                        if '.' not in item:
                            return int(item)
                        else:
                            return float(item)

                    # or sequence
                    elif ',' in item:
                        items = item.split(',')
                        return tuple(seq_dive(iitem) for iitem in items)

                    else:
                        return item

                elif isinstance(item, list):
                    return [seq_dive(iitem) for iitem in item]

            for string in self.args.parameter:

                if '=' not in string:
                    print('parameters should be specified in the format: -p name=value')
                    raise SystemExit

                name, valstring = string.split('=')

                if '[' in valstring and ']' in valstring:
                    listParser = NestedExpr("[", "]")
                    valstring = listParser.parseString(valstring).asList()[0]

                valstring = seq_dive(valstring)
                pdict.update({name: valstring})

            for exp in self._runnable_reqs.experiments:
                self._paramset_reqs.update({exp: pdict})

        self._requests_resolved = True

    # # deprecated in favor of .common.parse_runnable_parameters() which doesn't require a  live module
    # def _parse_runnable_parameters(self):
    #     """ get default parameters """
    #     malformed = []
    #     for r in self._runnable_reqs.values():
    #         if not hasattr(self._live_modules[r.name], 'main'):
    #             malformed.append(r.name)
    #         else:
    #             if PYTHONVERSION.major == 3:
    #                 sig = inspect.signature(self._live_modules[r.name].main)
    #                 r.default_params = {parameter.name: parameter.default for parameter in
    #                                     sig.parameters.values()}
    #             elif PYTHONVERSION.major == 2:
    #                 sig = inspect.signature(r.module.main)
    #                 r.default_params = {parameter: sig.defaults[i] for i, parameter in enumerate(sig.args)}
    #
    #     for r in malformed:
    #         del self._runnables_avail[r]

    def _process_parameters(self):
        """see if any experiments have asked for param-sets """

        for r in self._runnable_reqs.values():

            rp = {}

            if r.name in self._paramset_reqs and not self.debug:
                # # do parameterized runs
                rp.update(self._paramset_reqs[r.name])
            else:
                # # do default run
                rp.update(r.default_params)

            for key, value in rp.items():
                if isinstance(value, str) or not hasattr(value, '__iter__'):
                    rp[key] = [value, ]


            # get number of subexperiments
            names = tuple(rp.keys())
            items = [rp[n] for n in names]
            tvec = product(*items)

            psets = []
            for el in tvec:
                psets.append({name: el[i] for i, name in enumerate(names)})

            # check whether we're doing multiple trials
            if r.name in self._trial_reqs and not self.debug:
                multiplier = self._trial_reqs[r.name]
            else:
                multiplier = 1

            # crate jobs and append to queue
            rep_ind = 0
            for repeats in range(multiplier):
                for ps in psets:
                    j = Job(r, ps, rep_ind)
                    self._run_q.update({j.name: j})
                    rep_ind += 1

    def _run_basic_prelude(self):

        # clear .xanity/tmp:
        if os.path.isdir(os.path.join(self.paths.tmp)):
            shutil.rmtree(os.path.join(self.paths.tmp))
        os.mkdir(os.path.join(self.paths.tmp))

        # start writing logs to /.xanity/tmp
        self._attach_root_logger_fh()

        # set global root dirs and do some basic path operations
        os.chdir(self.paths.project_root)

        # print some info
        self.log(
            '\n'
            '################################################################################\n'
            '## \n'
            '## \'run\' called at {} \n'
            '## xanity-args:{}\n'
            '## xanity_root: {} \n'
            '################################################################################\n'
            '\n'.format(
                datetime.datetime.fromtimestamp(time.mktime(self._start_time)).strftime('%Y-%m-%d %H:%M:%S'),
                vars(self.args),
                self.paths.project_root)
        )

    def _run_exp_prelude(self):
        """
            bunch of meta-level setup for subsequent experiments
        """
        from .xanity_env import dump_pip_requirements, save_conda_snapshot
        if not self.debug:
            # dump bookkeeping
            self._archive_source_tree()
            dump_pip_requirements()
            save_conda_snapshot()

        exps_to_run = self._run_q.experiments
        paramsets = exps_to_run.param_dict

        # print number of subexperiments found:
        self.log(
            "\n"
            "################################################################################\n"
            "################################################################################\n"
            "###\n"
            "###                 going to run {} experiments in total... \n"
            "###\n"
            "################################################################################\n"
            "################################################################################\n".format(
                len(exps_to_run))

        )
        for exp, params in paramsets.items():
            if len(params) > 1:
                self.log(
                    '\n'
                    '################################################################################\n'
                    '##  experiment: {} has {} subexperiments:\n'.format(exp, len(params))
                    + '\n'.join(['##     {}_{}: {}'.format(exp, i, p) for i, p in enumerate(params)]) + '\n'
                    + '################################################################################'
                )

    def _run_anal_prelude(self):
        pass

    def _run_all_exps(self):
        """
        do all experiments
        """

        self._run_exp_prelude()
        for i, experiment in enumerate(self._run_q.experiments.values()):
            with self.act_tags(ACTIVITIES.EXP):
                self._conditional_run(experiment, i)

    def _run_all_anals(self):
        """
        do all analyses
        """

        self._run_anal_prelude()

        for i, analysis in enumerate(self._run_q.analyses.values()):
            with self.act_tags(ACTIVITIES.ANAL):
                self._conditional_run(analysis, i)

    def _conditional_run(self, job, index):
        """
        First, check to see whether the job needs to run at all. Then check whether it can run, based on
        its dependencies.
        :param job:
        :param index:
        :return:
        """
        try:
            found_data = self.__cache['data'][job.runnable.name][job.runnable.hash][
                hash_parameters(job.parameters)]

            if all([p in found_data for p in job.runnable.products]) and not self._force:
                self.warn('Reusing existing data for \'{}\'. '
                      'To force xanity to re-run, use the --force argument.'.format(job.runnable.name))
                return

        except:
            pass

        for d in job.runnable.dependencies:
            pass

        self._live_modules[job.runnable.name] = get_live_module(job.runnable.module_path)
        self._run_one_job(job, index)

    def _run_one_job(self, job, index):

        self.status = Status()

        self.status.job = job
        self.status.xanity_info = os.path.join(self.status.job.data_dir, DIRNAMES.XANITY_INFO)
        self.status.xanity_variables = os.path.join(self.status.job.data_dir, DIRNAMES.SAVED_VARS)

        # set some environment variablves for the benefit of any downstream shells
        os.environ['XANITY_DEBUG'] = str(self.debug)
        os.environ['XANITY_DATA_DIR'] = str(job.data_dir)

        self._make_exp_dirs(job)

        if not self.debug:
            # create per-run log file
            tfh = logging.FileHandler(
                filename=os.path.join(
                    self.status.job.data_dir, DIRNAMES.XANITY_INFO,
                    self.run_id + '_' + job.name + '_' + str(index) + DIRNAMES.LOG_SUFFIX))
            tfh.setFormatter(logging.Formatter(eval(LOG_FORMAT)))
            tfh.setLevel(logging.DEBUG)
            self.logger.addHandler(tfh)

        if isinstance(job.runnable, Experiment):
            log_tot = len(self._run_q.experiments)
            log_header = EXPERIMENT_LOG_HEADER
        elif isinstance(job.runnable, Analysis):
            log_tot = len(self._run_q.analyses)
            log_header = ANALYSIS_LOG_HEADER

        self.log(log_header.format(
            job.name, index+1, log_tot, self.status.job.parameters))

        opwd = os.getcwd()
        successful = False
        os.chdir(self.status.job.data_dir)
        snap = os.listdir()

        try:
            sys.path.append(job.runnable.module_path)

            with self.act_tags(ACTIVITIES.EXP):
                if self._profile:
                    profile.runctx(
                        'module.main(**paramdict)',
                        {},
                        {'module': self._live_modules[job.runnable.name], 'paramdict': self.status.parameters},
                        os.path.join(self.status.job.data_dir, self.run_id + '.profile'))
                else:
                    self._live_modules[job.runnable.name].main(**self.status.job.parameters)

            successful = True

        except (KeyboardInterrupt, BdbQuit) as e:
            self.log('experiment terminated by user.')
            self._wrap_job(success=False, prerun_snap=snap)
            raise e

        except Exception as e:
            successful = False
            self.logger.error('caught exception:')
            self.logger.error(e)

            if self.debug or self.debug_xanity:
                self._wrap_job(success=False, prerun_snap=snap)
                raise e

        finally:

            self._wrap_job(success=successful, prerun_snap=snap)

            # detach logger file
            if 'tfh' in locals() and hasattr(self, 'logger'):
                self.logger.removeHandler(tfh)

            sys.path.remove(job.runnable.module_path)
            os.chdir(opwd)
            self.status = Status()

            gc.collect()

    def _wrap_job(self, success, prerun_snap):
        from .xanity_data import register_data_obj
        job = self.status.job

        # notify user and update job
        if success:
            self.log('experiment {} was successful'.format(job.name))
            with open(os.path.join(self.status.xanity_info, 'successful'), 'w+') as f:
                pass

            job.success = True
            job.products = job.runnable.products

            # look for files produced during run:
            af = [f for f in os.listdir(job.data_dir) if f not in prerun_snap]
            for a in af:
                if 'path://' + a not in job.runnable.products:
                    self.warn('It looks like runnable \'{}\' has created a file/dir called \'{}\'.\n'
                          'Please use the \'xanity.save_path()\' interface to declare it.'.format(job.runnable.name, a))
                job.products.extend(['path://' + f for f in af])

            # create data entries for each product
            for p in job.products:
                if p.startswith('path://'):
                    name = p
                    path = p.split('path://')[-1]
                    if not os.path.isabs(path):
                        path = os.path.join(self.status.job.data_dir, path )
                else:
                    name = p
                    path = os.path.join(self.status.xanity_variables, p+'.dill')

                register_data_obj(
                    DataRecord(
                        name,
                        path,
                        job)
                )
        else:
            job.success = False
            job.products = []
            self.log('run {} was NOT successful'.format(job.name))
            with open(os.path.join(job.data_dir, DIRNAMES.XANITY_INFO, 'unsuccessful'), 'w+') as f:
                pass
            self.save_xanity_obj_panic()

        # save job.  This overwrites a pickled job written during _make_exp_dirs()
        pickle_dump(job, os.path.join(self.status.xanity_info, DIRNAMES.PICKLED_JOB))



    def _init_logger(self):
        """ setup a logger ... """
        # create logger
        self.logger = logging.getLogger('xanity_logger')
        self.logger.handlers = []
        self.logger.setLevel(logging.DEBUG)

        lsh = logging.StreamHandler(sys.stdout)
        lsh.setFormatter(logging.Formatter(eval(LOG_FORMAT)))
        lsh.setLevel(logging.DEBUG)
        self.logger.addHandler(lsh)

    def _attach_root_logger_fh(self):
        root_handle = logging.FileHandler(filename=os.path.join(self.paths.tmp, self.run_id + DIRNAMES.LOG_SUFFIX))
        root_handle.setFormatter(logging.Formatter(eval(LOG_FORMAT)))
        root_handle.setLevel(logging.DEBUG)
        self.logger.addHandler(root_handle)

    def _load_requested_modules(self):
        """
        docstring
        :return:
        """

        for name, fullpath in [(r.name, r.module_path) for r in self._runnable_reqs.values()]:
            self._live_modules[name] = get_live_module(fullpath)

    def _archive_source_tree(self):

        if self.debug:
            return None

        archive_file = os.path.join(self.paths.xanity_data, 'source_archive.tar.gz')
        last_hash_file = self.paths.last_source_hash
        current_source_hash = digest_string(''.join([str(r.hash) for r in self._runnables_avail.values()]))

        if os.path.isfile(archive_file) and os.path.isfile(last_hash_file):
            if current_source_hash == open(last_hash_file, 'r').read():
                self.log('reusing existing source archive')
                return archive_file

        self.log('creating gzipped archive of source code')

        def filterfn(tarinfo):
            return None if any([fnmatch.fnmatch(tarinfo.name, pattern) for pattern in SOURCE_IGNORE]) else tarinfo

        with tarfile.open(archive_file, mode='w:gz') as tarball:
            tarball.add(self.paths.project_root, arcname=self.project_name, filter=filterfn)

        with open(last_hash_file, 'w+') as f:
            f.write(current_source_hash)

        return archive_file

    def _resolve_xanity_root(self):
        """attempts to ground the current xanity within a tree

                look at given disposition and determine a xanity root

                """

        root = in_xanity_tree()

        if not root:
            if self.verbosity > 1:
                print('not presently within a xanity tree')

            # look into 'callers' first, then 'importers' for hints
            cands = set(filter(lambda item: bool(item), [in_xanity_tree(hint) for hint in self._importers]))
            if len(cands) > 1:
                print('multiple xanity project roots found... usure what to do')
                raise NotImplementedError
            if len(cands) == 1:
                root = cands.pop()

            if not root and self._importers:
                # now try importers
                cands = set(filter(lambda item: bool(item), [in_xanity_tree(hint) for hint in self._importers]))
                if len(cands) > 1:
                    print('multiple xanity project roots found... usure what to do')
                    raise NotImplementedError
                if len(cands) == 1:
                    root = cands.pop()

        if root:
            # # compute paths from root
            relpaths = ConstantSet({
                key: os.path.join(root, value)
                for key, value in vars(RELATIVE_PATHS).items()})

            xanity_paths = ConstantSet({
                key: os.path.join(root, value)
                for key, value in vars(XANITY_PATHS).items()})

            # now apply it to self
            self.paths = relpaths + xanity_paths
            self.project_name = self.paths.project_root.split('/')[-1]

    def register_import(self):
        tb = inspect.stack()
        for frame in tb:
            if frame[4] and any(['import xanity' in c for c in frame[4]]):
                caller = frame[1]
                if caller not in self._importers:
                    self._importers.add(caller)

    def register_loaded_data(self, df):
        from .xanity_data import register_data_obj, fetch_job
        if not df.empty:
            for index, r in df.iterrows():
                v = r['variable_name']
                vp = r['variable_path']
                j = r['job']
                entry = DataRecord(v, vp, j)
                register_data_obj(entry)
                self.status.job.loaded_data.append(entry.hash)

    def _make_exp_dirs(self, job):

        exp_root = os.path.join(job.data_dir)
        xanity_vars = os.path.join(exp_root, DIRNAMES.SAVED_VARS)
        info = os.path.join(exp_root, DIRNAMES.XANITY_INFO)

        try:
            os.makedirs(os.path.join(self.paths.run_data, job.runnable.name))
        except OSError:
            pass

        try:
            os.makedirs(xanity_vars)
            os.makedirs(info)

            # save a copy of job immediately. This will be overwritten during self._wrap_job()
            pickle_dump(job, os.path.join(info, DIRNAMES.PICKLED_JOB))

        except OSError:
            edie('run data directory was already created... something\'s wrong')

        for root, subd, files in os.walk(self.paths.tmp):

            relpath = root.split(self.paths.tmp)[1]

            for sd in subd:
                os.mkdir(job.data_dir / info / relpath / sd)

            for ff in files:
                os.link(
                    os.path.join(root, ff),
                    os.path.join(info, relpath, ff)
                )

    def list_avail_experiments(self):
        if not self.paths.project_root:
            raise XanityNoProjectRootError

        return list_modules_at_path(self.paths.experiments)

    def list_avail_analyses(self, names=None):
        if not self.paths.project_root:
            raise XanityNoProjectRootError

        return list_modules_at_path(self.paths.analyses)

    @property
    def shell_prelude(self):
        if os.path.isfile(self.paths.shell_prelude):
            return open(self.paths.shell_prelude, mode='r').read()
        else:
            return None

    @property
    def shell_conclude(self):
        if os.path.isfile(self.paths.shell_conclude):
            return open(self.paths.shell_conclude, mode='r').read()
        else:
            return None

    @shell_prelude.setter
    def shell_prelude(self, value):
        if isinstance(value, str):
            value = [value]
        else:
            value = list(value)

        result = open(self.paths.shell_prelude, mode='w').write('\n'.join(value))

        if result is None:
            print('wrote new shell prelude script. please restart xanity.')
            raise SystemExit

        else:
            raise NotImplementedError

    @shell_conclude.setter
    def shell_conclude(self, value):
        if isinstance(value, str):
            value = [value]
        else:
            value = list(value)

        result = open(self.paths.shell_prelude, mode='w').write('\n'.join(value))
        if result is None:
            print('wrote new shell conclude script. please restart xanity.')
            raise SystemExit

        else:
            raise NotImplementedError

    def run(self, clargs=None):
        from .xanity_env import correct_environment
        from . import _commands
        if self.action and self.action not in _commands.init+_commands.setup:
            correct_environment()

        self._invocation = INVOCATION.HOOK
        self._invoker = get_external_caller()
        self._parse_args(clargs)
        self._absolute_trigger()

    def cmd(self, command):
        from .__main__ import main

        self._invocation = INVOCATION.COMMAND
        self._parse_args(command)
        main()

    def internal_run(self):
        self._absolute_trigger()

    def metarun(self, experiment=None, parameters=None, host=None, remote_command=''):
        raise NotImplemented

        # global invocation
        # self._invocation = INVOCATION.HOOK
        # invocation = INVOCATION.HOOK
        # self._invoker = get_external_caller()
        #
        # caller = os.path.split(get_external_caller())[-1].split('.py')[0]
        # if caller in self.experiments_req:
        #     del self.experiments_req[caller]
        #
        # if host is not None:

            # if not os.path.isdir(self.exp_data_dir):
            #     os.makedirs(self.exp_data_dir)
            #
            # self._run_basic_prelude()
            #
            # self.log('sending source to {}...'.format(host))
            # subprocess.check_call(
            #     self._condabashcmd('rsync -avzhuP --info=progress2 {} {}:~/XANITY_REMOTE/ {}'.format(
            #         self.paths.project_root,
            #         host,
            #         ' '.join(['--exclude={}'.format(item.lstrip('/')) for item in SOURCE_IGNORE])
            #     ))
            # )
            #
            # self.log('checking xanity on {}...'.format(host))
            # try:
            #     subprocess.check_call(
            #         shsplit(
            #             'ssh {} \'bash -lc "which xanity"\''.format(
            #                 host,
            #             )
            #         ))
            #
            # except subprocess.CalledProcessError:
            #     print('xanity doesn\'t appear to be installed on host')
            #     raise SystemExit
            #
            # if parameters is not None:
            #
            #     # self._exp_paramset_requests[experiment] = parameters
            #     # self._resolve_requests()
            #     # self._purge_dangling_experiments()
            #     # self._load_required_modules()
            #     # self._resolve_associations()
            #     self._process_parameters()
            #
            #     for pset in self.experiments[experiment].paramsets:
            #         cmd = remote_command + ' ' if remote_command else ''
            #         cmd += 'xanity run {} -D XANITY_REMOTE/{} --initialize --setup'.format(
            #             experiment,
            #             os.path.split(self.paths.project_root)[-1],
            #         )
            #
            #         for name, val in pset.items():
            #             if isinstance(val, tuple):
            #                 val = str(val).rstrip(')').lstrip('(')
            #             cmd += ' -p {}={}'.format(name, val)
            #
            #         self.log('executing \'{}\' on {}...'.format(cmd, host))
            #         subprocess.check_call(
            #             shsplit(
            #                 'ssh {} \'bash -lc "{}"\''.format(
            #                     host,
            #                     cmd,
            #                 )
            #             )
            #         )

        # else:
        #
        #     if parameters is not None:
        #         self._paramset_reqs[experiment] = parameters
        #     self._absolute_trigger()

    def save_xanity_obj_panic(self):
        if ACTIVITIES.EXP in self.act_tags:
            attrs_to_skip = ['logger', 'avail_experiments', 'avail_analyses']
            targ = {}
            for item in dir(self):
                if item not in attrs_to_skip:
                    targ[item] = getattr(self, item)
            pickle_dump(targ, os.path.join(self.status.xanity_info, 'xanity_panic.dill'))

    def log(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def experiment_parameters(self, parameters_dict):
        caller_name = file2mod(get_external_caller())
        self._paramset_reqs[caller_name] = parameters_dict

    def trials(self, number_of_trials):
        caller_name = file2mod(get_external_caller())
        self._trial_reqs.update({caller_name: number_of_trials})
