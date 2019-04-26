import tempfile
import shutil
import subprocess

from copier import copy

from .naming import Naming


def clone(url, checkout=None):
    location = tempfile.mkdtemp()
    shutil.rmtree(location)  # Path must not exists
    subprocess.check_call(["git", "clone", url, location])
    if checkout:
        subprocess.check_call(["git", "checkout", checkout], cwd=location)
    return location


def run(opts):
    bindings = {
        'folder': opts.get('<folder>'),
        'app': opts.get('--app'),
        'proj': Naming.camelize(opts.get('<folder>').split('/')[-1]),
        'bare': opts.get('--bare'),
        'pypi': opts.get('--pypi'),
        'repo': opts.get('--repo'),
        'checkout': opts.get('--checkout')
    }

    bare_list = [
        'horn_proj/models/user.py.tmpl',
        'horn_proj/schemas/user.py.tmpl',
        'horn_proj/views/user.py.tmpl',
        'horn_proj/views/session.py.tmpl',
        'horn_proj/helpers.py.tmpl',
        'horn_test/views/test_user.py.tmpl',
        'horn_test/views/test_session.py.tmpl',
    ]

    if bindings.get('repo'):
        location = clone(bindings.get('repo'), bindings.get('checkout'))
        copy(location, bindings.get('folder'), data=bindings)
    else:
        if bindings.get('bare'):
            copy('./templates/horn_proj', bindings.get('folder'), data=bindings, exclude=bare_list)
        else:
            copy('./templates/horn_proj', bindings.get('folder'), data=bindings)
