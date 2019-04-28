from pampy import match, _, TAIL
from copier import copy

from horn.utils import Naming, get_proj_info, get_tpl_path, merge_fields


TPL_PATH = get_tpl_path('..', 'templates')

TYPES = {
    'integer': 'Integer',
    'float': 'Float',
    'number': 'Number',
    'decimal': 'Decimal',
    'boolean': 'Boolean',
    'string': 'String',
    'date': 'Date',
    'time': 'Time',
    'timedelta': 'TimeDelta',
    'datetime': 'DateTime',
    'uuid': 'UUID',
    'tuple': 'Tuple',
    'list': 'List',
    'dict': 'Dict',
    'map': 'Mapping',
    'url': 'Url',
    'email': 'Email',

    'nest': 'Nested',

    'required': 'required',
    'dump': 'dump_only',
    'load': 'load_only'
}


def run(opts):
    bindings = {
        'module': opts.get('<module>'),
        'module_file': Naming.underscore(opts.get('<module>')),
        'model': opts.get('--model'),
        'fields': parse_fields(opts.get('<fields>')),
    }

    bindings.update(get_proj_info())

    copy(f'{TPL_PATH}/schema', f'{bindings.get("app")}/schemas', data=bindings)


def validate_type(arg):
    if arg not in TYPES:
        print(f'field type error: {arg}')
        exit(1)
    return TYPES.get(arg)


def validate_attr(*args):
    affix = ['required', 'dump', 'load']
    for arg in args:
        if arg not in affix:
            print(f'field type error: {":".join(args)}')
            exit(1)

    return dict(zip(args, [True for i in args]))


def parse_fields(fields):
    attrs = [f.split(':') for f in fields]
    return [match(attr,
                [_, _],               lambda x, y: {'field': x, 'type': validate_type(y)},  # noqa
                [_, 'nest', _],       lambda x, schema: {'field': x, 'type': 'Nested', 'schema': f'{Naming.camelize(schema)}Schema'},  # noqa
                [_, 'nest', _, TAIL], lambda x, schema, t: merge_fields({'field': x, 'type': 'Nested', 'schema': f'{Naming.camelize(schema)}Schema'}, validate_attr(*t)),  # noqa
                [_, _, TAIL],         lambda x, y, t: merge_fields({'field': x, 'type': validate_type(y)}, validate_attr(*t))  # noqa
    ) for attr in attrs]
