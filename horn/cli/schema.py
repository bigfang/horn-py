from pampy import match, _, TAIL
from copier import copy

from horn.naming import Naming
from horn.path import TPL_PATH, get_location
from horn.tpl import get_proj_info, merge_fields, validate_type, validate_attr, validate_opts


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
}

AFFIXES = ('none', 'required', 'dump', 'load', 'exclude')


def run(opts):
    validate_opts(opts)

    bindings = {
        'module': opts.get('<module>'),
        'singular': Naming.underscore(opts.get('<module>')),
        'model': opts.get('--model'),
        'fields': parse_fields(opts.get('<fields>')),
    }
    bindings.update(get_proj_info())
    bindings.update(collect_meta(bindings.get('fields')))

    location = get_location(bindings) or TPL_PATH
    copy(f'{location}/gen', '.', data=bindings,
         exclude=['*/services/*', '*/models/*', '*/views/*', 'test/*'])


def collect_meta(fields):
    dump_only = []
    load_only = []
    exclude = []
    for field in fields:
        check_meta_keys(field)
        if field.get('dump'):
            dump_only.append(field['field'])
        elif field.get('load'):
            load_only.append(field['field'])
        elif field.get('exclude'):
            exclude.append(field['field'])
    return {
        'dump_only': dump_only,
        'load_only': load_only,
        'exclude': exclude,
    }


def parse_fields(fields):
    attrs = [f.split(':') for f in fields]
    return [match(
        attr,
        [_, _],               lambda x, y: {'field': x, 'type': validate_type(y, TYPES)},  # noqa: E241,E272
        [_, 'nest', _],       lambda x, schema: {'field': x, 'type': 'Nested', 'schema': f'{Naming.camelize(schema)}Schema'},  # noqa: E241,E272
        [_, 'nest', _, TAIL], lambda x, schema, t: merge_fields({'field': x, 'type': 'Nested', 'schema': f'{Naming.camelize(schema)}Schema'}, validate_attr(AFFIXES, *t)),  # noqa: E241,E272
        [_, _, TAIL],         lambda x, y, t: merge_fields({'field': x, 'type': validate_type(y, TYPES)}, validate_attr(AFFIXES, *t))  # noqa: E241,E272
    ) for attr in attrs]


def check_meta_keys(field):
    meta_keys = {'dump', 'load', 'exclude'}
    intersection = meta_keys & set(field)
    if len(intersection) > 1:
        print(f'Error: Field attributes error, {intersection} conflict')
        exit(1)
