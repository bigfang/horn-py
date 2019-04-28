import secrets
import json

from copier import copy

from horn.utils import Naming, clone, get_tpl_path


TPL_PATH = get_tpl_path('..', 'templates')


def run(opts):
    bindings = {
        'folder': opts.get('<folder>'),
        'secret_key': secrets.token_urlsafe(12),
        'prod_secret_key': secrets.token_urlsafe(24)
    }

    if not opts.get('<repo>'):
        bindings.update({
            'app': opts.get('--app'),
            'proj': opts.get('--proj') or Naming.camelize(opts.get('<folder>').split('/')[-1]),
            'bare': opts.get('--bare'),
            'pypi': opts.get('--pypi'),
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

        if bindings.get('bare'):
            copy(f'{TPL_PATH}/new', bindings.get('folder'), data=bindings, exclude=ignore_list)
        else:
            copy(f'{TPL_PATH}/new', bindings.get('folder'), data=bindings, include=['log/'])
    else:
        bindings.update({
            'repo': opts.get('<repo>'),
            'checkout': opts.get('--checkout'),
            'json': opts.get('--json'),
            'file': opts.get('--file'),
        })

        attrs = json.loads(bindings.get('json'))
        if bindings.get('file'):
            with open(bindings.get('file')) as f:
                conf = json.load(f)
                attrs.update(conf)
        attrs.update({
            'folder': bindings.get('folder'),
            'app': Naming.humanize(bindings.get('folder').split('/')[-1]),
            'proj': Naming.camelize(bindings.get('folder').split('/')[-1])
        })

        location = clone(bindings.get('repo'), bindings.get('checkout'))
        copy(f'{location}/new', bindings.get('folder'), data=attrs)
