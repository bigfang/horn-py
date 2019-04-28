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
    data = toml.load('./project.toml')
    return data.get('project')
