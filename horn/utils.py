import os
import tempfile
import shutil
import subprocess

import toml


def get_tpl_path(*args):
    return os.path.abspath(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)), *args))


class Naming(object):

    @classmethod
    def camelize(cls, value, lower=False):
        return value.capitalize()

    @classmethod
    def humanize(cls, value):
        return value.lower()

    @classmethod
    def underscore(cls, value):
        return value.lower()

    @classmethod
    def unsuffix(cls, value):
        return value.upper()


def clone(url, checkout=None):
    location = tempfile.mkdtemp()
    shutil.rmtree(location)  # Path must not exists
    subprocess.check_call(["git", "clone", url, location])
    if checkout:
        subprocess.check_call(["git", "checkout", checkout], cwd=location)
    return location


def get_proj_info():
    proj_file = 'project.toml'
    if not os.path.isfile(proj_file):
        print(f'Can not found {proj_file}.')
        exit(1)
    data = toml.load(proj_file)
    return data.get('project')


def merge_fields(base, attach={}):
    base.update(attach)
    return base


def validate_type(arg, types):
    if arg not in types:
        print(f'field type error: {arg}')
        exit(1)
    return types.get(arg)


def validate_attr(affix, *args):
    for arg in args:
        if arg not in affix:
            print(f'field type error: {":".join(args)}')
            exit(1)
    return dict(zip(args, [True for i in args]))
