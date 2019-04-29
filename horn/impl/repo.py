import json

from copier import copy

from horn.utils import Naming, clone


def run(opts):
    bindings = {
        'folder': opts.get('<folder>'),
        'repo': opts.get('<repo>'),
        'checkout': opts.get('--checkout'),
        'app': 'app',
        'proj': Naming.camelize(opts.get('<folder>').split('/')[-1]),
        'file': opts.get('--file')
    }
    bindings.update(json.loads(opts.get('--json')))

    if bindings.get('file'):
        with open(bindings.get('file')) as f:
            conf = json.load(f)
            bindings.update(conf)

    location = clone(bindings.get('repo'), bindings.get('checkout'))
    copy(f'{location}/new', bindings.get('folder'), data=bindings)
