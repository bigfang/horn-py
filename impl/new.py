import secrets

from copier import copy

from .utils import Naming, clone


def run(opts):
    bindings = {
        'folder': opts.get('<folder>'),
        'app': opts.get('--app'),
        'proj': opts.get('--proj') or Naming.camelize(opts.get('<folder>').split('/')[-1]),
        'bare': opts.get('--bare'),
        'pypi': opts.get('--pypi'),
        'repo': opts.get('--repo'),
        'checkout': opts.get('--checkout'),
    }
    bindings.update({
        'secret_key': secrets.token_urlsafe(12),
        'prod_secret_key': secrets.token_urlsafe(24)
    })

    ignore_list = [
        f'{bindings.get("app")}/helpers.py',
        '*/models/user.py',
        '*/views/user.py',
        '*/views/session.py',
        '*/schemas/user.py',
        '*/schemas/session.py',
        'test/views/test_user.py',
        'test/views/test_session.py'
    ]

    if bindings.get('repo'):
        location = clone(bindings.get('repo'), bindings.get('checkout'))
        copy(location, bindings.get('folder'), data=bindings)
    else:
        if bindings.get('bare'):
            copy('./templates/horn_proj', bindings.get('folder'), data=bindings, exclude=ignore_list)
        else:
            copy('./templates/horn_proj', bindings.get('folder'), data=bindings, include=['log/'])
