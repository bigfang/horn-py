from pampy import match, _, TAIL
from copier import copy

from horn.utils import Naming, get_proj_info, get_tpl_path, merge_fields


TPL_PATH = get_tpl_path('..', 'templates')

TYPES = {
    'integer': 'Integer',
    'float': 'Float',
    'decimal': 'Decimal',
    'boolean': 'Boolean',
    'string': 'String',
    'text': 'Text',
    'date': 'Date',
    'time': 'Time',
    'datetime': 'DateTime',
    'uuid': 'UUID',
    'json': 'JSON',
    'array': 'ARRAY',

    'ref': 'reference',
    'default': 'default'
}


def run(opts):
    bindings = {
        'module': opts.get('<module>'),
        'module_file': Naming.underscore(opts.get('<module>')),
        'table': opts.get('<table>'),
        'fields': parse_fields(opts.get('<fields>'))
    }

    bindings.update(get_proj_info())

    copy(f'{TPL_PATH}/model', f'{bindings.get("app")}/models', data=bindings)


def validate_type(arg):
    if arg not in TYPES:
        print(f'field type error: {arg}')
        exit(1)
    return TYPES.get(arg)


def validate_attr(*args):
    affix = ['uniq', 'nonull', 'index']
    for arg in args:
        if arg not in affix:
            print(f'field type error: {":".join(args)}')
            exit(1)

    return dict(zip(args, [True for i in args]))


def parse_fields(fields):
    attrs = [f.split(':') for f in fields]
    return [match(attr,
                [_, _],              lambda x, y: {'field': x, 'type': validate_type(y)},  # noqa
                [_, 'ref', _],       lambda x, table: {'field': x, 'type': validate_type('ref'), 'table': table},  # noqa
                [_, 'ref', _, TAIL], lambda x, table, t: merge_fields({'field': x, 'type': validate_type('ref'), 'table': table}, validate_attr(*t)),  # noqa
                [_, _, 'default', _],       lambda x, y, default: {'field': x, 'type': validate_type(y), 'default': default},  # noqa
                [_, _, 'default', _, TAIL], lambda x, y, default, t: merge_fields({'field': x, 'type': validate_type(y), 'default': default}, validate_attr(*t)),  # noqa
                [_, _, TAIL],        lambda x, y, t: merge_fields({'field': x, 'type': validate_type(y)}, validate_attr(*t))  # noqa
    ) for attr in attrs]
