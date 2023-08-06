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

from __future__ import print_function

import fnmatch
import os
import os.path as path
import hashlib
import sys
import cloudpickle as pickle
import inspect
import time
import argparse
import ast
import shelve
import re

from bdb import BdbQuit
from collections import namedtuple
from collections import OrderedDict


from sys import version_info as PYTHONVERSION

from .constants import ConstantSet, RUN_DIR_REGEX

if PYTHONVERSION.major == 2:
    import imp
    from codecs import open

elif PYTHONVERSION.major == 3:
    import importlib


class XanityDeprecationError(NotImplementedError):
    pass


class XanityNotOrientedError(RuntimeError):
    pass


class XanityNoProjectRootError(RuntimeError):
    pass


class XanityUnknownActivityError(ValueError):
    pass


class XanityCommand(object):
    def __init__(self, aliases, parser, entry, description):
        if isinstance(aliases, str):
            aliases = [aliases]

        self.name = aliases[0]
        self.aliases = list(set(aliases[1:]))
        self.parser = parser
        self.entry = entry
        self.description = description

    def __iter__(self):
        for a in [self.name] + self.aliases:
            yield a

    def __add__(self, other):
        assert isinstance(other, XanityCommand)
        return CommandSet([self, other])

    def __contains__(self, item):
        if item is None:
            return False
        return True if any([fnmatch.fnmatch(item.lower(), a) for a in [self.name] + self.aliases]) else False

    def __eq__(self, other):
        if isinstance(other, str):
            return True if any([fnmatch.fnmatch(other, a) for a in [self.name] + self.aliases]) else False
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, str):
            return False if any([fnmatch.fnmatch(other, a) for a in [self.name] + self.aliases]) else True
        else:
            return True

    def __repr__(self):
        aas = '|'.join(self.aliases)
        return self.name + '|' + aas if aas else self.name


class CommandSet(ConstantSet):
    def __init__(self, command_list):
        if not isinstance(command_list, dict):  # used for addition of CommandSets
            d = {}
            for item in command_list:
                if isinstance(item, XanityCommand):
                    d.update({item.name: item})
                elif isinstance(item, (tuple, list)):
                    if isinstance(item[0], str):
                        item[0] = [item[0]]
                    d.update({item[0][0]: XanityCommand(*item)})
        else:
            d = command_list
        super(CommandSet, self).__init__(d)

    def __add__(self, other):
        assert isinstance(other, (CommandSet, XanityCommand))
        d = {}
        d.update(vars(self))
        if isinstance(other, CommandSet):
            d.update(vars(other))
        elif isinstance(other, XanityCommand):
            d.update({other.name: other})
        return CommandSet(d)

    def __contains__(self, item):
        return any([item in cmd for cmd in vars(self).values()])

    def __iter__(self):
        for c in vars(self).values():
            yield c

    def __getitem__(self, item):
        cands = [cmd for cmd in vars(self).values() if item in cmd]
        if len(cands) > 1:
            return [cand for cand in cands if cand != '*'][0]
        elif len(cands) == 1:
            return cands[0]
        else:
            raise KeyError


def _generate_root_help(commands):
    text = "available commands include:\n"

    for item in vars(commands).values():
        aliases = list(item.aliases)[1:]
        if len(aliases) > 1:
            if len(aliases) > 3:
                aliases = aliases[:3]
            text += "    {:<7}{:<25} {:}\n\n".format(item.name, '[' + '|'.join(aliases) + ']', item.description)
        else:
            text += "    {:<7}{:<25} {:}\n\n".format(item.name, '', item.description)

    return text


class RootParser(argparse.ArgumentParser):
    def __init__(self, commands):
        super(RootParser, self).__init__(prog='xanity',
                                         description='manage ecosystem of experiments and analyses',
                                         add_help=False)
        self.add_argument('action', nargs='?', help=_generate_root_help(commands))
        self.add_argument('--xanity-root', nargs='?', help='specify xanity project tree')
        self.add_argument('--version', '-V', action='store_true')
        self.add_argument('--verbosity', '-v', action='store', help='specify or increase verbosity')
        self.add_argument('--debug', action='store_true',
                          help='run xanity experiments in debugging mode; experiment code may print additional output'
                               ' or behave differently. Parameterized sets will reduce to a single experiment.')
        self.add_argument('--debug-xanity', '--xanity-debug', '-X', action='store_true',
                          help='Enable debugging output of xanity itself.')
        self.__commands = commands

    def parse_known_args(self, *args, **kwargs):
        kn, unk = super(RootParser, self).parse_known_args(*args, **kwargs)

        if kn.action in self.__commands:
            return self.__commands[kn.action].parser().parse_known_args(*args, **kwargs)
        else:
            return kn, unk


CacheObjectEntry = namedtuple('CacheObjectEntry', ['ID', 'hash', 'objectpath', 'linked_file'])
CacheDataEntry = namedtuple('CacheDataEntry', ['data_hash', 'data_path'])


class Cache(shelve.DbfilenameShelf):
    def __init__(self, *args, **kwargs):
        super(Cache, self).__init__(*args, **kwargs)

    def fetch_object(self, ID, hash):
        entry = self[ID]
        if not os.path.exists(entry.linked_file):
            del self[ID]
            raise KeyError

        if hash == entry.hash:
            try:
                return pickle_load(entry.objectpath)
            except:
                os.remove(entry.objectpath)
                del self[ID]
        else:
            raise KeyError

    def store_object(self, ID, hash, object, linked_file):
        from . import _x as X
        assert os.path.exists(linked_file), 'every entry must be tied to a file'
        object_location = os.path.join(X.paths.cache_contents, digest_string(ID))
        entry = CacheObjectEntry(ID, hash, object_location, linked_file)
        pickle_dump(object, object_location)
        self[entry.ID] = entry


class Runable(object):
    def __init__(self, module_path):
        self.module_path = module_path
        self.name = os.path.split(module_path)[-1].split('.py')[0]
        with open(module_path, 'r') as f:
            self.code = ast.parse(f.read(), module_path)
        self.default_params = parse_runnable_parameters(self)
        self.dependencies = parse_runnable_dependencies(self)
        self.products = parse_runnable_products(self)
        self.hash = hash(self)
        assert not self._malformed()

    def _malformed(self, runnable=None):

        if runnable is None:
            runnable = self

        assert 'main' in [node.name for node in ast.iter_child_nodes(runnable.code) if hasattr(node, 'name')], \
            'runnable {} does not have a \'main\' function'.format(runnable.name)

        if isinstance(self, Analysis):
            assert self.dependencies is not None

        return False

    def __hash__(self):
        if hasattr(self, 'hash'):
            return self.hash
        else:
            self.hash = int(digest_obj(self.code), 16)
            return self.hash


class Experiment(Runable):
    pass


class Analysis(Runable):
    pass


class RunnableList(OrderedDict):

    @property
    def experiments(self):
        return RunnableList([r for r in self if isinstance(r, Experiment)])

    @property
    def analyses(self):
        return RunnableList([r for r in self if isinstance(r, Analysis)])


class Job(object):
    def __init__(self, runnable, parameters, repeat_index=0):
        from . import _x as x
        self.runnable = runnable
        self.parameters = parameters
        self.name = '_'.join([runnable.name, str(repeat_index)])
        self.runid = '_'.join([x.run_id, self.name])
        self.data_dir = os.path.join(x.paths.run_data, runnable.name, self.runid)
        self.success = None
        self.timed_fn_results = {}
        self.products = []
        self.loaded_data = []
        self.hash = hash(self)

    def __hash__(self):
        if hasattr(self, 'hash'):
            return self.hash
        else:
            el = []
            el.append(str(self.runnable.hash))
            el.append(digest_obj(self.parameters))
            el.append(digest_obj(self.loaded_data))

            hash = int(digest_string(''.join(el)), 16)
            self.hash = hash
            return self.hash

    def update(self, dict_of_values):
        for key in dict_of_values.keys():
            assert key in self.runnable.default_params, '\'{}\' is not an Experiment parameter'.format(key)
        self.param_dict.update(dict_of_values)


class JobList(OrderedDict):

    @property
    def experiments(self):
        return JobList({
            k: v for k, v in self.items() if isinstance(v.runnable, Experiment)
        })

    @property
    def analyses(self):
        return JobList({
            k: v for k, v in self.items() if isinstance(v.runnable, Analysis)
        })

    @property
    def param_dict(self):
        subct = {}
        for r in self.values():
            if r.runnable.name not in subct:
                subct[r.runnable.name] = [r.parameters]
            else:
                subct[r.runnable.name] += [r.parameters]
        return subct


class DataRecord(object):
    """
    xanity data object representing saved output of a runnable.
    items are included by calls to xanity.save_data()
    """
    def __init__(self, item, path, job):

        self.name = item
        self.path = path
        self.generator_name = job.runnable.name
        self.generator_hash = job.runnable.hash
        self.generator_params = job.parameters
        self.param_hash = hash_parameters(job.parameters)
        self.upstream_data = job.loaded_data
        self.hash = hash(self)

    def __hash__(self):
        if hasattr(self, 'hash'):
            return self.hash
        else:
            el = ''

            el += self.name
            el += str(self.generator_hash)
            el += str(self.param_hash)
            el += ''.join([str(h) for h in self.upstream_data])

            self.hash = int(digest_string(el), 16)
            return self.hash

    def __eq__(self, other):
        return True if hash(self) == hash(other) else False


class ContextStack(list):
    def __init__(self):
        super(ContextStack, self).__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pop()

    def __call__(self, activity):
        self.append(activity)
        return self


class Status(object):
    def __init__(self):
        self.job = None
        self.xanity_info = None
        self.xanity_variables = None


class Alias(object):
    def __init__(self, aliases):
        aliases = [aliases] if isinstance(aliases, str) else aliases
        self.aliases = tuple(aliases)

    def __contains__(self, item):
        return True if item.lower() in self.aliases else False

    def __repr__(self):
        return self.aliases[0]

    def __add__(self, other):
        assert isinstance(other, (Alias, list, tuple))
        return self.aliases + tuple(other)

    def __iter__(self):
        return self.aliases.__iter__()

    def __eq__(self, other):
        return self.__contains__(other)


def hash_parameters(paramdict):
    return int(digest_string(str(paramdict).strip()), 16)


def get_live_package_object(package_path):
    spec = importlib.util.spec_from_file_location(
        path.split(package_path)[-1].rstrip('/'),
        location=package_path + os.sep + '__init__.py')
    package = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(package)
    return package


def get_live_module(module_path):

    parent = os.path.sep.join(module_path.split(os.path.sep)[:-1])

    if parent not in sys.path:
        sys.path.append(parent)
        pop = True
    else:
        pop = False

    module_name = file2mod(module_path)
    if PYTHONVERSION.major == 2:
        module = imp.load_source(module_name, module_path)
    else:
        spec = importlib.util.spec_from_file_location(module_name, location=module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    if pop:
        sys.path.remove(parent)
    return module


def digest_path(path_root):
    hashes = []
    for root, sdirs, files in os.walk(path_root):
        sdirs.sort()
        files.sort()

        for sd in sdirs:
            hashes += [digest_path(os.path.join(root, sd))]

        for ff in files:
            hashes += [digest_file(os.path.join(root, ff))]

    hasher = hashlib.sha1()
    for item in hashes:
        hasher.update(item.encode('utf-8'))

    return hasher.hexdigest()


def digest_file(filename):
    if PYTHONVERSION.major == 3:
        return hashlib.sha1(open(filename, 'rb').read()).hexdigest()
    elif PYTHONVERSION.major == 2:
        return hashlib.sha1(open(filename, 'r', encoding='utf-8').read()).hexdigest()


def digest_string(string):
    return hashlib.sha1(string.encode('utf-8')).hexdigest()


def digest_obj(object):
    s = pickle.dumps(object)
    return hashlib.sha1(s).hexdigest()


def pickle_dump(item, filepath):
    if pickle.__name__ == 'dill':
        return pickle.dump(item, open(filepath, mode='wb'), 2)
    elif pickle.__name__ == 'cloudpickle':
        return pickle.dump(item, open(filepath, mode='wb'), protocol=2)


def pickle_load(filepath):
    if pickle.__name__ == 'dill':
        return pickle.load(open(filepath, mode='rb'), 2)
    elif pickle.__name__ == 'cloudpickle':
        return pickle.load(open(filepath, mode='rb'))


def file2mod(filepath):
    return os.path.split(filepath)[-1].split('.py')[0]


def list_modules_at_path(pathspec, names=None):
    assert os.path.isdir(pathspec)
    mods = [file.split('.')[0] for file in fnmatch.filter(os.listdir(pathspec), '[!_]*.py')]
    mods.sort()
    mods = list(filter(lambda item: item in names, mods)) if names else mods
    paths = [path.join(pathspec, mod + '.py') for mod in mods]
    return tuple(zip(mods, paths))


def get_external_frame():
    from . import _x
    from . import __file__ as x_root
    x_root = os.path.dirname(x_root)

    tb_stack = inspect.stack()

    for f in tb_stack:
        if x_root not in f.filename:
            return f

    if _x.debug_xanity:
        print('\n'.join([item.__str__() for item in tb_stack]))
    raise BaseException('xanity could not find external caller\'s file name')


def get_external_caller():
    return get_external_frame().filename


def get_arg_names():
    from . import __file__ as x_path
    x_path = os.path.dirname(x_path)
    acceptible_fns = ['save_variable', 'save_checkpoint', 'my_timed_function']
    f = get_external_frame()
    ccs = ''.join(f.code_context)
    if not any([s in ccs for s in acceptible_fns]):
        edie('looks like you might have renamed a xanity function on import.\n'
             'For xanity to work reliably, you must not rename them')
    name = inspect.stack()[1].function
    code = ast.parse(''.join(f.code_context).lstrip(), filename=f.filename, mode='eval')

    args = []
    kwargs = {}

    for n in ast.walk(code):
        if isinstance(n, ast.Call) and n.func.attr == name:
            if n.args:
                for a in n.args:
                    args.append(
                        str(a.s) if isinstance(a, ast.Str) else
                        a.id if isinstance(a, ast.Name) else
                        [e.id for e in a.elts] if isinstance(a, ast.List) else
                        None
                        )

            if n.keywords:
                for kw in n.keywords:
                    kwargs.update({kw.arg: kw.value.id if isinstance(kw.value, ast.Name) else
                                            kw.value.s if isinstance(kw.value, ast.Str) else
                                            [e.id for e in kw.value.elts] if isinstance(kw.value, ast.List) else
                                            None})

            break

    return args, kwargs


def find_xanity_root(hint=None):
    if hint and not hint.startswith('/'):
        hint = os.path.normpath(os.path.join(os.getcwd(), hint))

    bot = os.getcwd() if not hint else os.path.expanduser(os.path.expandvars(hint))
    maxdepth = 7
    parts = bot.split(os.sep)
    cur_dep = len(parts)

    root = None
    for d in range(cur_dep, cur_dep - maxdepth - 1, -1):
        if d > cur_dep or d == 0:
            break
        targ = os.sep + os.path.join(*parts[:d])
        dirs = os.listdir(targ)
        if '.xanity' in dirs:
            root = targ

    return root


def confirm(prompt=None, default_response=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', default_response=True)
    Create Directory? [y]|n:
    True
    >>> confirm(prompt='Create Directory?', default_response=False)
    Create Directory? [n]|y:
    False
    >>> confirm(prompt='Create Directory?', default_response=False)
    Create Directory? [n]|y: y
    True

    """

    if prompt is None:
        prompt = 'Confirm?'

    if default_response:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')

    try:
        while True:
            if PYTHONVERSION.major > 2:
                ans = input(prompt)
            else:
                ans = raw_input(prompt)

            if not ans:
                return default_response

            if ans not in ['y', 'Y', 'n', 'N']:
                print
                'please enter y or n.'
                continue

            if ans == 'y' or ans == 'Y':
                return True

            if ans == 'n' or ans == 'N':
                return False

            time.sleep(1e-3)

    except (KeyboardInterrupt, BdbQuit) as e:
        raise SystemExit

    print('')


def in_xanity_tree(file_or_path=None):
    """
    test a file/dir to see if it's in a xanity tree.

    :param file_or_path: hint for searching

    :returns: root of hinted xanity project tree
    """
    result = None

    if not file_or_path:
        file_or_path = os.getcwd()

    else:
        if os.path.isfile(file_or_path):
            file_or_path = os.path.split(file_or_path)[0]
        elif os.path.isdir(file_or_path):
            pass
        else:
            file_or_path = os.getcwd()

    path_parts = file_or_path.split('/')

    for i in range(len(path_parts))[::-1]:
        test_path = '/' + os.path.join(*path_parts[:i + 1])
        if os.path.isdir(os.path.join(test_path, '.xanity')):
            result = test_path
            break

    return result


def parse_runnable_dependencies(runnable):
    """
    go through runnable's code and look for xanity.load_data() calls.

    ensure that all required data either exists, or will be generated during the run

    :return:
    """
    required_data = {}

    mainfn = None
    for root in ast.iter_child_nodes(runnable.code):
        if hasattr(root, 'name') and root.name == 'main':
            mainfn = root

    if mainfn is None:
        edie('xanity runnable \'{}\' does not have a \'main\' function'.format(runnable.module_path))

    for n in ast.walk(mainfn):
        if isinstance(n, ast.Call):
            if hasattr(n.func, 'value'):
                if hasattr(n.func.value, 'id'):
                    if n.func.value.id == 'xanity':
                        if n.func.attr == 'load_data':
                            if n.args:
                                d_exps = n.args[0]
                            else:
                                try:
                                    d_exps = [item.value for item in n.keywords if item.arg == 'selection'][0]
                                except:
                                    edie('bad load_data() call in {}:{}'.format(runnable.module_path, n.lineno))

                            if not isinstance(d_exps, ast.Dict):
                                raise ImportError
                            else:
                                for key, val in zip(d_exps.keys, d_exps.values):
                                    if isinstance(val, ast.Str):
                                        val = ast.List([val])
                                    if key.s not in required_data:
                                        required_data[key.s] = set([v.s for v in val.elts])
                                    else:
                                        required_data[key.s] = required_data[key.s] | set([v.s for v in val.elts])

    return required_data


def parse_runnable_products(runnable):
    """
    go through runnable's code and look for xanity.save_variable() calls.

    :return:
    """
    data_products = []

    mainfn = None
    for root in ast.iter_child_nodes(runnable.code):
        if hasattr(root, 'name') and root.name == 'main':
            mainfn = root

    if mainfn is None:
        edie('xanity runnable {} does not have a \'main\' function')

    for n in ast.walk(mainfn):
        if isinstance(n, ast.Call) \
                and hasattr(n.func, 'value')\
                and hasattr(n.func.value, 'id')\
                and n.func.value.id == 'xanity':

            if n.func.attr == 'save_variable':

                if n.args:
                    data_products.append(n.args[0].id)

                else:
                    try:
                        data_products.append([item.value.id for item in n.keywords if item.arg == 'value'][0])
                    except:
                        edie('bad save_variable() call in {}:{}'.format(runnable.module_path, n.lineno))

            if n.func.attr == 'save_path':
                if n.args:
                    if isinstance(n.args[0], ast.Str):
                        list = ['path://' + n.args[0].s]
                    else:
                        list = ['path://' + item.s for item in n.args[0]]

                else:
                    if not any([item.arg == 'path' for item in n.keywords]):
                        edie('bad save_path() call in {}:{}'.format(runnable.module_path, n.lineno))

                    list = [item.value for item in n.keywords if item.arg == 'path'][0]

                    if isinstance(list, ast.Str):
                        list = ['path://' + list]
                    else:
                        list = ['path://' + item.s for item in list.elts]

                data_products.extend(list)

    return data_products


def parse_runnable_parameters(runnable):
    """
        go through runnable's code and return the default parameters to main().

        :return:
        """
    params = {}

    mainfn = None
    for root in ast.iter_child_nodes(runnable.code):
        if hasattr(root, 'name') and root.name == 'main':
            mainfn = root

    if mainfn is None:
        edie('xanity runnable {} does not have a \'main\' function')

    for k, v in zip(mainfn.args.args, mainfn.args.defaults):
        if isinstance(v, ast.Str):
            v = v.s

        elif isinstance(v, ast.Num):
            v = v.n

        else:
            edie('unrecognized parameters to main() in runnable \'{}\''.format(runnable.module_path))

        params.update({k.arg: v})

    return params


def warn(message):
    print(message, file=sys.stderr)


def die(message):
    from . import _x as x
    x.log(message)
    raise SystemExit(0)


def edie(message, code=os.EX_USAGE):
    warn(message)
    raise SystemExit(code)
