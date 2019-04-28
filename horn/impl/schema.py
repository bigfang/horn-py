from pampy import match, _, TAIL
from copier import copy

from horn.utils import (Naming, get_proj_info, get_tpl_path, merge_fields,
                        validate_type, validate_attr)


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

AFFIX = ('required', 'dump', 'load')


def run(opts):
    bindings = {
        'module': opts.get('<module>'),
        'module_file': Naming.underscore(opts.get('<module>')),
        'model': opts.get('--model'),
        'fields': parse_fields(opts.get('<fields>')),
    }

    bindings.update(get_proj_info())

    copy(f'{TPL_PATH}/schema', f'{bindings.get("app")}/schemas', data=bindings)


def parse_fields(fields):
    attrs = [f.split(':') for f in fields]
    return [match(attr,
                [_, _],               lambda x, y: {'field': x, 'type': validate_type(y, TYPES)},  # noqa
                [_, 'nest', _],       lambda x, schema: {'field': x, 'type': 'Nested', 'schema': f'{Naming.camelize(schema)}Schema'},  # noqa
                [_, 'nest', _, TAIL], lambda x, schema, t: merge_fields({'field': x, 'type': 'Nested', 'schema': f'{Naming.camelize(schema)}Schema'}, validate_attr(AFFIX, *t)),  # noqa
                [_, _, TAIL],         lambda x, y, t: merge_fields({'field': x, 'type': validate_type(y, TYPES)}, validate_attr(AFFIX, *t))  # noqa
    ) for attr in attrs]
