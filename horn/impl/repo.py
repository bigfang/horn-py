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
    opt_json = json.loads(opts.get('--json'))
    check_conflict(opt_json)
    bindings.update(opt_json)

    if bindings.get('file'):
        with open(bindings.get('file')) as f:
            conf = json.load(f)
            check_conflict(conf)
            bindings.update(conf)

    location = clone(bindings.get('repo'), bindings.get('checkout'))
    copy(f'{location}/new', bindings.get('folder'), data=bindings)


def check_conflict(opt):
    only_keys = ["folder", 'repo', 'checkout', 'file']
    for ok in only_keys:
        if ok in opt:
            print(f'Conflict field found: {{{ok}: {opt.get(ok)}}}')
            exit(1)
