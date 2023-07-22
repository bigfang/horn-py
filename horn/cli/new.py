import secrets
from pathlib import Path

import inflection
from copier import run_copy

from horn.path import TPL_PATH


def run(opts):
    bindings = {
        'target': Path(opts.get('<target>')).resolve().name,
        'secret_key': secrets.token_urlsafe(12),
        'prod_secret_key': secrets.token_urlsafe(24),
        'app': inflection.underscore(opts.get('--app')),
        'proj': inflection.camelize(opts.get('--proj') or Path(opts.get('<target>')).resolve().name),
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
            'tests/views/test_user.py',
            'tests/views/test_session.py'
        ])

    run_copy(f'{TPL_PATH}/new', opts.get('<target>'), data=bindings, exclude=ignore_list)
