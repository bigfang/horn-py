import secrets

import inflection
from copier import copy

from horn.path import TPL_PATH


def run(opts):
    bindings = {
        'target': opts.get('<target>'),
        'secret_key': secrets.token_urlsafe(12),
        'prod_secret_key': secrets.token_urlsafe(24),
        'app': opts.get('--app'),
        'proj': opts.get('--proj') or inflection.camelize(opts.get('<target>').split('/')[-1]),
        'bare': opts.get('--bare'),
        'pypi': opts.get('--pypi'),
    }

    ignore_list = ['*/__pycache__/*']
    if bindings.get('bare'):
        ignore_list.extend([
            f'{bindings.get("app")}/helpers.py',
            '*/models/user.py',
            '*/views/user.py',
            '*/views/session.py',
            '*/schemas/user.py',
            '*/schemas/session.py',
            'test/views/test_user.py',
            'test/views/test_session.py'
        ])

    copy(f'{TPL_PATH}/new', bindings.get('target'), data=bindings, exclude=ignore_list)
