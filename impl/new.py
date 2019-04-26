from copier import copy

from .naming import Naming


def run(opts):
    bindings = {
        'folder': opts.get('<folder>'),
        'app': opts.get('--app') or 'app',
        'proj': Naming.camelize(opts.get('<folder>').split('/')[-1]),
        'bare': opts.get('--bare'),
        'pypi': opts.get('--pypi') or 'pypi.org',
        'repo': opts.get('--repo')
    }

    bindings.update(opts)

    bare_list = [
        'horn_proj/models/user.py.tmpl',
        'horn_proj/schemas/user.py.tmpl',
        'horn_proj/views/user.py.tmpl',
        'horn_proj/views/session.py.tmpl',
        'horn_proj/helpers.py.tmpl',
        'horn_test/views/test_user.py.tmpl',
        'horn_test/views/test_session.py.tmpl',
    ]

    if bindings.get('bare'):
        copy('./templates/horn_proj', bindings.get('folder'), data=bindings, exclude=bare_list)
    else:
        copy('./templates/horn_proj', bindings.get('folder'), data=bindings)
