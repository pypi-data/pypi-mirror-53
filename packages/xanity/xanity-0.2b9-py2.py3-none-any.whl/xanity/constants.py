import os
from argparse import Namespace


class ConstantSet(Namespace):
    def __init__(self, constants):
        super(ConstantSet, self).__init__(**constants)

    def __add__(self, other):
        d = vars(self)
        d.update(vars(other))
        return ConstantSet(d)


SOURCE_IGNORE = [
    'data/runs',
    'data/saved',
    'data/persistent',
    '.xanity',
    '.git',
    '.idea',
    '.gitignore',
]

RELATIVE_PATHS = ConstantSet({
    'src': 'src/',
    'include': 'include/',
    'experiments': 'experiments/',
    'analyses': 'analyses/',
    'run_data': 'data/runs/',
    'persistent_data': 'data/persistent/',
    'saved_data': 'data/saved/',
    'project_root': '',
    'xanity_data': '.xanity/',
    'checkpoints': 'data/checkpoints/',
    'tmp': '.xanity/tmp/',
    'conda_env_file': 'conda_environment.yaml',
})

XANITY_PATHS = ConstantSet({
    'conda_env': os.path.join(RELATIVE_PATHS.xanity_data, 'conda_env'),
    'conda_env_python': os.path.join(RELATIVE_PATHS.xanity_data, 'conda_env', 'bin', 'python'),
    'conda_hash': os.path.join(RELATIVE_PATHS.xanity_data, 'conda.md5'),
    'env_hash': os.path.join(RELATIVE_PATHS.xanity_data, 'env_state.md5'),
    'shell_prelude': os.path.join(RELATIVE_PATHS.xanity_data, 'shell_prelude'),
    'shell_conclude': os.path.join(RELATIVE_PATHS.xanity_data, 'shell_conclude'),
    'last_source_hash': os.path.join(RELATIVE_PATHS.xanity_data, 'last_source_hash'),
    'last_pip_hash': os.path.join(RELATIVE_PATHS.xanity_data, 'last_pip_hash'),
    'rcfile': os.path.join(RELATIVE_PATHS.xanity_data, 'bashrc'),
    'cache': os.path.join(RELATIVE_PATHS.xanity_data, 'cache'),
    'cache_index': os.path.join(RELATIVE_PATHS.xanity_data, 'cache', 'index.dbm'),
    'cache_contents': os.path.join(RELATIVE_PATHS.xanity_data, 'cache', 'contents'),
})

ACTIVITIES = ConstantSet({
    'CONSTRUCT': 'const',  # only during constructor call
    'ORIENT': 'orient',  # only while orienting  !! this should be the only opportunity for recursive calls
    'RUN': 'run',  # only during _absolute_trigger()
    'ABORT': 'abort',  # signals a fatal error
    'MOD_LOAD': 'lm',  # loading a live module obj...  !! also an opportunity for recursive calls
    'EXP': 'exp',  # during experimentation
    'ANAL': 'anal',  # during analysis
})

DIRNAMES = ConstantSet({
    'SAVED_VARS': "xanity_variables",
    'RUN_PARAMETERS': 'xanity_parameters.dill',
    'PICKLED_JOB': 'xanity_job.dill',
    'LOG_SUFFIX': '.xanity.log',
    'SELF_REPLICATION': 'xanity_self_replication',
    'XANITY_INFO': 'xanity_info',
})

INVOCATION = ConstantSet({
    'COMMAND': 'module_command',
    'HOOK': 'hook',
})

EXPERIMENT_LOG_HEADER = \
    """


    ################################################################################
    ##
    ##   Starting experiment \'{}\' ({} of {}):
    ##   {}
    ##
    ################################################################################
    """

ANALYSIS_LOG_HEADER = \
    """


    ################################################################################
    ##
    ##   Starting analysis \'{}\' ({} of {}): 
    ##   {}
    ##
    ################################################################################
    """

RUN_DIR_REGEX = r'^(\d{4}-\d{2}-\d{2}-\d{6}(?:-debug)?)_(\S*)_(\d+)$'
LOG_FORMAT = 'self.run_id + \'.%(relativeCreated)d [xanity]: %(message)s\''