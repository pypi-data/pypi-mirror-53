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

import subprocess
import pkg_resources
import shutil
import glob

from shlex import split as shsplit

from .common import *
from .constants import DIRNAMES

helptext = """
env setup :  create a conda environment inside an existing xanity directory tree 

usage:  xanity env setup [help]

xanity env setup assumes you're in a xanity tree (generally speaking)
"""

example_conda_env_file = \
    '''
    ### example conda_env file
    ### place in xanity project root
    
    channels:
        - javascript              
    dependencies:                
        - python=3.4                
        - bokeh=0.9.2              
        - numpy=1.9.*               
        - nodejs=0.10.*            
        - flask                    
        - pip:                     
            - Flask-Testing          
            - \"--editable=git+ssh://git@gitlab.com/lars-gatech/pyspectre.git#egg=pyspectre\"
            - \"git+ssh://git@gitlab.com/lars-gatech/libpsf.git#egg=libpsf\"
    '''


def bashcmd(cmd):
    # ## using neither -i or -l results in loss of access to 'conda' command
    # ## using the -i option results in bash complaining about lack of ioctl
    # ## using the -l option for now :/
    return shsplit('bash -lc \'{}\''.format(cmd))


# def condacmd(cmd):
#     from . import _xanity_obj as X
#     if os.path.isfile(X.paths.rcfile):
#         return shsplit('bash --rcfile {} -lc \'PYTHONNOUSERSITE=1 {} \''.format(rcfile, cmd))
#     else:
#         return shsplit('bash -lc \'PYTHONNOUSERSITE=1 {}\''.format(cmd))


def envcmd(cmd):
    # ## using neither -i or -l results in loss of access to 'conda' command
    # ## using the -i option results in bash complaining about lack of ioctl
    # ## using the -l option for now :/
    #
    # ## failing to 'deactivate' the conda session results in pausing of the job (if using from terminal)
    # ## so be sure to 'conda deactivate'
    from . import _x as x

    # if os.path.isfile(x.paths.rcfile):
    #     return shsplit('bash --rcfile {} -ic \'conda activate {} && {} \''.format(rcfile,x.paths.conda_env, cmd))
    # else:
    return shsplit('bash -lc \'conda activate {} && {} && conda deactivate\''.format(x.paths.conda_env, cmd))


def check_environment(env_path=None):
    interpreter = os.path.abspath(sys.executable)

    if not env_path:
        from . import _x as x
        env_path = x.paths.conda_env
        if x.verbosity >= 2:
            x.log('current interpreter: {}'.format(interpreter))

    if str(env_path) in interpreter:
        return True
    else:
        return False


def correct_environment():
    from . import _x as x

    if not check_environment():
        python_exe = x.paths.conda_env_python
        verbosity = x.verbosity
        x.close()

        if not os.path.isfile(python_exe):
            print('you\'re not in the right env and it doesn\'t look like one has been setup.'
                  'Try runing \'xanity env setup\'.')
            raise SystemExit(1)

        else:
            if verbosity >= 2:
                print('you\'re not in the right env... starting over from the right one...')
            try:
                if '/xanity/__main__.py' in sys.argv[0]:
                    raise SystemExit(subprocess.call(
                        envcmd(
                            '{} -m xanity {}'.format(
                                python_exe,
                                ' '.join(sys.argv[1:]))
                        ),
                    ))
                else:
                    raise SystemExit(subprocess.call(
                        envcmd(
                            '{} {}'.format(
                                python_exe,
                                ' '.join(sys.argv))
                        ),
                    ))
                
            except SystemExit as e:
                raise e

            except BaseException:
                print('\n\n'
                      'you were not inside the correct conda environment and we had some trouble running inside'
                      'the right one. \n'
                      'If you\'re using an IDE or calling a script directly, \n'
                      'please be sure you\'re using the python inside the \n'
                      'conda environment at path:\n{}\n\n'.format(python_exe))
                raise SystemExit(os.EX_CONFIG)


def check_xanity_ver():
    try:
        sys_xanity = os.environ['XANITY_HOST_VER']

    except BaseException:
        sys_xanity = subprocess.check_output(shsplit('bash -l xanity --version')).decode().split('Version:')[1].split()[
            0]

    myver = sys.modules['xanity'].__version__
    result = myver == sys_xanity
    print('\n'
          'system xanity version: {}\n'
          'conda env xanity vers: {}\n'
          '\n'.format(sys_xanity, myver)
          )

    return result


def check_conda_env():
    from . import _x as x

    conda_env_hash_file = x.paths.env_hash

    if not os.path.isfile(conda_env_hash_file):
        return False

    conda_env_hash = hash_conda_env()
    with open(conda_env_hash_file, mode='r') as f:
        saved_hash = f.read()

    return conda_env_hash == saved_hash


def hash_conda_env():
    from . import _x as x

    conda_env_path = x.paths.conda_env

    try:
        # conda_env_contents = ''.join(sorted(str(subprocess.check_output([
        #     # 'bash', '-c', 'source xanity-enable-conda.sh 2>&1 /dev/null && conda list -n {}'.format(conda_env_name)
        #     'bash', '-lc', 'conda list -n {}'.format(conda_env_name)  # xanity(bash) makes sure conda is on path :)
        # ]).decode()).replace(' ', '').split()))
        conda_env_contents = ''.join(sorted(str(
            subprocess.check_output(
                bashcmd('conda list -p {}'.format(conda_env_path))
            ).decode()).replace(' ', '').split()))

    except subprocess.CalledProcessError:
        return None
    conda_env_contents = conda_env_contents.replace(' ', '')
    return digest_string(conda_env_contents)


def create_local_rcfile():
    """
    this is required in order for \'xanity sesh\' to work
    :return:
    """
    from . import _x as x

    orig_rc = '$HOME/.bashrc'
    target_rc = x.paths.rcfile

    orig_rc = os.path.expandvars(os.path.expanduser(orig_rc))
    if not os.path.isfile(orig_rc):
        print('user doesn\'t seem to have a .bashrc file.')
    with open(orig_rc, 'r') as f:
        file = f.readlines()

    file.append('conda activate {}\n'.format(x.paths.conda_env))
    with open(target_rc, 'w') as f:
        f.writelines(file)

    return


def check_conda_file():
    from . import _x as x

    conda_file_hash = x.paths.conda_hash

    if not os.path.isfile(conda_file_hash):
        return False

    conda_hash = hash_conda_env_file()
    with open(conda_file_hash, mode='r') as f:
        saved_hash = f.read()
    return conda_hash == saved_hash


def check_conda():
    return check_conda_env() and check_conda_file()


def hash_conda_env_file():
    from . import _x as x
    return digest_file(x.paths.conda_env_file)


def freeze_conda():
    from . import _x as x

    conda_hash_file = x.paths.conda_hash
    env_hash_file = x.paths.env_hash

    open(conda_hash_file, mode='w').write(hash_conda_env_file())
    open(env_hash_file, mode='w').write(hash_conda_env())

    while not os.path.isfile(conda_hash_file):
        time.sleep(0.1)
    while not os.path.isfile(env_hash_file):
        time.sleep(0.1)

    assert check_conda_file()


def save_conda_snapshot():
    from . import _x as x

    archive_file = os.path.join(x.paths.tmp, 'conda_env_state.txt')
    with open(archive_file, 'w') as f:
        f.write(
            subprocess.check_output(bashcmd('conda list -p {}'.format(x.paths.conda_env)),
                                    stderr=subprocess.PIPE).decode()
        )
    print('saved output of \'conda list\'')
    return archive_file


def dump_pip_requirements():
    from . import _x as x

    # make requirements.txt
    archive_file = os.path.join(x.paths.tmp, 'pip-requirements.txt')

    # make requirements.txt
    reqs = subprocess.check_output(['pip', 'freeze']).decode()
    with open(archive_file, mode='w+') as reqsfile:
        reqsfile.write("""
                ############################################################################
                ##                                                                          ##
                ##   This is the state of the python environment running this experiment    ##
                ##   as understood by 'pip' and produced with the command `pip freeze`.     ##
                ##                                                                          ##
                 ###########################################################################
                """)
        reqsfile.write('\n')
        reqsfile.write(reqs)

    reqs = subprocess.check_output(['pip', 'freeze']).decode()
    with open(archive_file, mode='a+') as reqsfile:
        reqsfile.write(reqs)

    print('saved output of \'pip freeze\'')
    return archive_file


def disable_user_site():
    """
    make sure new env isn't using user-site behavior
    """
    from . import _x as x
    conda_env_path = x.paths.conda_env
    custom_site_file = os.path.join(glob.glob(os.path.join(conda_env_path, 'lib', 'python*'))[0], 'sitecustomize.py')
    custom_site_file_txt = (
        '\n'
        'import site\n'
        'import sys\n'
        'import os\n'
        '\n'
        'site.USER_BASE = \'/dev/null\'\n'
        'site.ENABLE_USER_SITE = False\n'
        'site.USER_SITE = \'/dev/null\'\n'
        '\n'
        'paths_to_remove = []\n'
        'for ddir in sys.path:\n'
        '    if os.path.expanduser(\'~/.local\') in ddir:\n'
        '        paths_to_remove.append(ddir)\n'
        '    elif \'xanity/src\' in ddir \\\n'
        '            and \'.xanity\' not in ddir \\\n'
        '            and \'xanity/src/xanity/xanity_self_replication\' not in ddir:\n'
        '        paths_to_remove.append(ddir)\n'
        '\n'
        'for ddir in paths_to_remove:\n'
        '    sys.path.remove(ddir)\n')

    print('writing custom site file: {}'.format(custom_site_file))
    with open(custom_site_file, 'w') as csf:
        csf.write(custom_site_file_txt)

    # also set PYTHONNOUSERSITE environment variable:
    # conda can save persistent variables in
    #    .../etc/conda/activate.d/env_vars.sh
    # and
    #    .../etc/conda/deactivate.d/env_vars.sh

    conda_env_activate_d = os.path.join(conda_env_path, 'etc', 'conda', 'activate.d')
    conda_env_deactivate_d = os.path.join(conda_env_path, 'etc', 'conda', 'deactivate.d')
    conda_env_activate_vars = os.path.join(conda_env_activate_d, 'env_vars.sh')
    conda_env_deactivate_vars = os.path.join(conda_env_deactivate_d, 'env_vars.sh')

    env_vars = {
        'PYTHONNOUSERSITE': '\'true\'',
        'PYTHONUSERBASE': '\'/dev/null\'',
    }

    if not os.path.isdir(conda_env_activate_d):
        os.makedirs(conda_env_activate_d)
    if not os.path.isdir(conda_env_deactivate_d):
        os.makedirs(conda_env_deactivate_d)

    print(('adding \'PYTHONNOUSERSITE\' and \'PYTHONUSERBASE\' to {} and {}'
           ).format(conda_env_activate_vars, conda_env_deactivate_vars))

    if not os.path.isfile(conda_env_activate_vars):
        with open(conda_env_activate_vars, 'w') as f:
            f.write(
                '#!/bin/sh\n'
                '\n'
            )
    with open(conda_env_activate_vars, 'a') as f:
        f.write(
            '\n' +
            '\n'.join(['export {}={}'.format(key, val) for key, val in env_vars.items()])
            + '\n'
        )

    if not os.path.isfile(conda_env_deactivate_vars):
        with open(conda_env_deactivate_vars, 'w') as f:
            f.write(
                '#!/bin/sh\n'
                '\n'
            )
    with open(conda_env_deactivate_vars, 'a') as f:
        f.write(
            '\n' +
            '\n'.join(['unset {}'.format(key) for key in env_vars.keys()])
            + '\n'
        )


def create_update_env(target_path, env_spec_filepath):
    python_executable = os.path.join(target_path, 'bin', 'python')

    if os.path.isfile(python_executable):
        # conda env exists
        # update conda env
        subprocess.check_call(
            bashcmd('conda env update --file {} -p {}'.format(env_spec_filepath, target_path))
            # ['bash', '-ic', 'conda env update --file {} -p {}'.format(env_spec_filepath, conda_env_path)]
        )
        print('updated conda env at {}'.format(target_path))

    else:

        # create conda env
        if os.path.isdir(target_path):
            shutil.rmtree(target_path)
        subprocess.check_call(
            bashcmd('conda env create --file {} -p {}'.format(env_spec_filepath, target_path))
            # ['bash', '-ic', 'conda env create --file {} -p {}'.format(env_spec_filepath, conda_env_path)]
        )
        print('created conda env at {}'.format(target_path))


def setup():
    from . import _x as x

    env_spec_filepath = x.paths.conda_env_file
    conda_env_path = x.paths.conda_env

    # check for 'conda_environment.yaml' file
    if not os.path.isfile(env_spec_filepath):
        print('could not find {} which contains the desired conda environment.'
              '  Please make one like this and put it in the xanity project root.\n\n'.format(env_spec_filepath))
        print(example_conda_env_file)
        raise SystemExit(1)

    else:
        print("found environment file: {}".format(env_spec_filepath))

    create_update_env(conda_env_path, env_spec_filepath)
    create_local_rcfile()


def xanity_available():
    from . import _x as x
    # test whether xanity is accessible in the env:
    try:
        result = subprocess.check_output(
            envcmd('python -s -m xanity --version'),
            stderr=subprocess.STDOUT)
        print(
            ('xanity {} is available in your env. If this is unexpected, call me.'
             ).format(result.decode().strip()))
        return True

    except subprocess.CalledProcessError as e:
        'xanity is not available in the env.'
        if x.verbosity > 1:
            print(e)
        return False


def install_xanity_into_env():
    # get the full path to this file :
    target_path = os.path.abspath(os.path.realpath(os.path.split(inspect.stack()[0][1])[0]))
    self_replication_subdir = DIRNAMES.SELF_REPLICATION

    while self_replication_subdir in target_path:
        print("running 'xanity env setup' from inside a xanity environment. Correcting paths...")
        parts = target_path.split(os.sep)
        repind = parts.index(self_replication_subdir)
        target_path = os.path.join(*parts[:repind])
        if parts[0] == '':
            target_path = os.path.sep + target_path

    target_path = os.path.join(target_path, self_replication_subdir)

    # print('setup_env replication source path: {}'.format(replication_source_path))
    assert (os.path.isdir(target_path)), 'could not find xanity self-replication package'

    # get this xanity version
    try:
        xanityver = pkg_resources.require("xanity")[0].version
        print('installing (-e) this xanity (version {}) into the new environment'.format(xanityver))

    except Exception:
        print(
            'this python interpreter does not have xanity installed. This is odd because a xanity script is running...')
        raise SystemExit

    subprocess.check_call(
        envcmd(
            'pip install -e {}'.format(target_path)
        ))

    return


def remove():
    from . import _x as x

    conda_env = x.paths.conda_env

    if os.path.isdir(conda_env):
        print('removing conda env: {}...'.format(conda_env))
        subprocess.check_call(bashcmd(
            'conda env remove -p {}'.format(conda_env)
        ))
        print('removed.')
    else:
        print('no environment to remove.')


def report_status():
    from . import _x as x

    conda_env = x.paths.conda_env
    conda_env_file = x.paths.conda_env_file

    setup_complete = True if check_conda else False
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode()
    installed_packages = [r.split('==')[0] for r in reqs.split()]

    req_packages = open(conda_env_file, 'r').read()
    req_packages = [line.lstrip(' -').split('#')[0].rstrip() if not line.lstrip().startswith('#') else '' for
                    line in req_packages.split('\n')]
    req_packages = list(filter(lambda item: bool(item), req_packages))

    req_start = [True if 'dependencies' in item else False for item in req_packages]
    req_start = req_start.index(True) + 1
    req_packages = req_packages[req_start:]

    missing_packages = [
        item if not any([item in item2 for item2 in installed_packages]) and 'python' not in item else None for
        item in req_packages]

    missing_packages = list(filter(lambda item: bool(item), missing_packages))
    print(
        '\n'
        '        conda env path: {}\n'
        '        setup complete: {}\n'
        '    installed packages: {}\n'
        '      missing packages: {}\n'
        ''.format(
            conda_env,
            setup_complete,
            len(installed_packages),
            '\n                        {}\n'.join(missing_packages) if missing_packages else None
        )
    )


class EnvRootParser(argparse.ArgumentParser):
    def __init__(self):
        from . import _root_parser
        super(EnvRootParser, self).__init__(prog='xanity-env',
                                            description='manipulate the conda environment inside the '
                                                        'xanity project',
                                            parents=[_root_parser],
                                            add_help=False)
        self.add_argument('subaction', help='manipulate the internal conda env')

    def parse_known_args(self, *args, **kwargs):
        kn, unk = super(EnvRootParser, self).parse_known_args(*args, **kwargs)
        if kn.subaction in subcommands:
            return subcommands[kn.subaction].parser().parse_known_args(*args, **kwargs)
        else:
            return kn, unk


class SetupParser(argparse.ArgumentParser):
    def __init__(self):
        super(SetupParser, self).__init__(prog='xanity-env-setup',
                                          description='setup the conda env inside the xanity project',
                                          parents=[EnvRootParser()])
        self.add_argument('directory', nargs='?', help='path to location of an existing xanity project')
        self.add_argument('--site', action='store_true', help='replace sitecustomize.py')


class RemoveParser(argparse.ArgumentParser):
    def __init__(self):
        super(RemoveParser, self).__init__(prog='xanity-env-remove',
                                           description='remove the conda environment inside the xanity project',
                                           parents=[EnvRootParser()])


class StatusParser(argparse.ArgumentParser):
    def __init__(self):
        super(StatusParser, self).__init__(prog='xanity-env-status',
                                           description='print the status of the conda environment inside the '
                                                       'xanity project.',
                                           parents=[EnvRootParser()])


class SessionParser(argparse.ArgumentParser):
    def __init__(self):
        from . import _root_parser
        super(SessionParser, self).__init__(prog='xanity-session',
                                            description='enter a bash session inside conda env',
                                            parents=[_root_parser])


def catchall_entry():
    EnvRootParser().print_help()
    raise SystemExit(0)


def setup_entry():
    from . import _x as x
    from . import new_xanity_session

    dirspec = x.args.directory

    if dirspec == 'help':
        SetupParser().print_help()
        raise SystemExit(0)

    elif dirspec:
        dirspec = os.path.expandvars(os.path.expanduser(dirspec))
        dirspec = os.path.realpath(dirspec)
        if not os.path.isdir(os.path.join(dirspec, '.xanity')):
            print('Specified directory doesn\'t seem to be a xanity project. Try running \'xanity init\'')
            raise SystemExit(1)
        os.chdir(dirspec)
        x = new_xanity_session()

    else:
        os.chdir(x.paths.project_root)

    if not os.path.isfile(x.paths.conda_env_python):
        # result = subprocess.call(['bash', setup_script, xanity_root])
        setup()
        freeze_conda()
        fresh = True
    else:
        fresh = False
        print('environment exists. checking status...')
        if not check_conda():
            print('updating environment...')

            setup()
            freeze_conda()

        else:
            print('looks like current setup is valid')

    if x.args.site or fresh:
        disable_user_site()

    if not xanity_available():
        install_xanity_into_env()


def remove_entry():
    from . import _x as x

    if 'help' in x.unknownargs:
        RemoveParser().print_help()
        raise SystemExit(0)
    remove()


def status_entry():
    from . import _x as x

    if 'help' in x.unknownargs:
        StatusParser().print_help()
        raise SystemExit(0)
    report_status()


def session_cmd_entry():
    from . import _x as x

    if 'help' in x.unknownargs:
        SessionParser().print_help()
        raise SystemExit(0)
    exit(subprocess.run(shsplit('bash --rcfile {}/.xanity/bashrc -i'.format(x.paths.project_root))).returncode)


def main():
    from . import _x as x
    from . import _commands

    assert x.args.action == _commands.env

    if x.args.subaction == 'help':
        EnvRootParser().print_help()
    elif x.args.subaction in subcommands:
        subcommands[x.args.subaction].entry()
    else:
        catchall_entry()


commands = CommandSet([
    # ([ aliases ], parser-type, entry-fn, description )
    (['env', 'environment'], EnvRootParser, main, 'run experiments/analyses'),
    (['sesh', 'session'], SessionParser, session_cmd_entry, 'enter bash prompt inside conda env')
])

subcommands = CommandSet([
    (['rm', 'remove'], RemoveParser, remove_entry, 'delete project\'s conda environment'),
    (['status'], StatusParser, status_entry, 'print status of project\'s conda environment'),
    (['setup'], SetupParser, setup_entry, 'setup the project\'s conda environment')
])

if __name__ == "__main__":
    main()
