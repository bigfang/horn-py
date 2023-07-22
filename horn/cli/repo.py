import json
from pathlib import Path

import inflection
from copier import run_copy

from horn.path import get_location


def run(opts):
    bindings = {
        'target': Path(opts.get('<target>')).resolve().name,
        'from': convert_path(opts.get('<from>')),
        'checkout': opts.get('<checkout>'),
        'app': 'app',
        'proj': inflection.camelize(Path(opts.get('<target>')).resolve().name),
        'file': opts.get('--file')
    }

    if bindings.get('file'):
        with open(bindings.get('file')) as f:
            conf = json.load(f)
            check_conflict(conf)
            bindings.update(conf)

    opt_json = json.loads(opts.get('--json'))
    check_conflict(opt_json)
    bindings.update(opt_json)

    location = get_location(bindings)
    try:
        run_copy(f'{location}/new', opts.get('<target>'), data=bindings, exclude=['*/__pycache__/*'])
    except ValueError:
        try:
            run_copy(f'{location}', opts.get('<target>'), data=bindings, exclude=['*/__pycache__/*'])
        except ValueError as err:
            print(f'Error: {err}')
            exit(1)


def convert_path(path):
    """
    >>> p = convert_path('foobar')
    >>> p.endswith('/foobar')
    True
    >>> convert_path('https://github.com')
    'https://github.com'
    """
    rv = path
    if not (path.startswith('http') or path.startswith('git@') or path.startswith('ssh://')):
        rv = str(Path(path).resolve())
    return rv


def check_conflict(opt):
    """
    >>> check_conflict({'app': 'foobar'})
    >>> try:
    ...     check_conflict({'from': 'bbb'})
    ... except:
    ...     pass
    Error: Conflict field found, {from: bbb}
    """
    reserved_words = ["target", 'from', 'checkout', 'file']
    for rw in reserved_words:
        if rw in opt:
            print(f'Error: Conflict field found, {{{rw}: {opt.get(rw)}}}')
            exit(1)
