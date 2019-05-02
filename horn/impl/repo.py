import json

from copier import copy

from horn.utils import Naming, get_location


def run(opts):
    bindings = {
        'target': opts.get('<target>'),
        'from': opts.get('<from>'),
        'checkout': opts.get('<checkout>'),
        'app': 'app',
        'proj': Naming.camelize(opts.get('<target>').split('/')[-1]),
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

    location = get_location(bindings)
    try:
        copy(f'{location}/new', bindings.get('target'), data=bindings)
    except ValueError as err:
        print(f'Error: {err}')


def check_conflict(opt):
    reserved_words = ["target", 'from', 'checkout', 'file']
    for rw in reserved_words:
        if rw in opt:
            print(f'Conflict field found: {{{rw}: {opt.get(rw)}}}')
            exit(1)
