import json

from copier import copy

from horn.utils import Naming, clone


def run(opts):
    bindings = {
        'folder': opts.get('<folder>'),
        'repo': opts.get('<repo>'),
        'checkout': opts.get('--checkout'),
        'json': opts.get('--json'),
        'file': opts.get('--file'),
    }

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
