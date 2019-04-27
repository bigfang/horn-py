import json

from copier import copy

from .utils import Naming, clone


def run(opts):
    bindings = {
        'folder': opts.get('<folder>'),
        'url': opts.get('<url>'),
        'ref': opts.get('<ref>'),
        'json': opts.get('--json') or {},
        'file': opts.get('--file'),
    }

    attrs = json.loads(bindings.get('json'))

    if bindings.get('file'):
        with open(bindings.get('file')) as f:
            conf = json.load(f)
            attrs.update(conf)

    location = clone(bindings.get('url'), bindings.get('ref'))
    copy(location, bindings.get('folder'), data=attrs)
