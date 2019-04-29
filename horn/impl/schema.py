from pampy import match, _, TAIL
from copier import copy

from horn.utils import (clone, Naming, get_proj_info, get_tpl_path,
                        merge_fields, validate_type, validate_attr)


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
    'load': 'load_only',
    'exclude': 'exclude'
}

AFFIX = ('none', 'required', 'dump', 'load', 'exclude')


def run(opts):
    bindings = {
        'module': opts.get('<module>'),
        'module_file': Naming.underscore(opts.get('<module>')),
        'model': opts.get('--model'),
        'fields': parse_fields(opts.get('<fields>')),
    }

    bindings.update(get_proj_info())
    bindings.update(collect_meta(bindings.get('fields')))

    location = TPL_PATH
    if bindings.get('repo'):
        location = clone(bindings.get('repo'), bindings.get('checkout'))
    copy(f'{location}/gen', '.', data=bindings,
         exclude=['*/services/*', '*/models/*', '*/views/*', 'test/*'])


def collect_meta(fields):
    dump_only = []
    load_only = []
    exclude = []
    for field in fields:
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
    return [match(attr,
                [_, _],               lambda x, y: {'field': x, 'type': validate_type(y, TYPES)},  # noqa
                [_, 'nest', _],       lambda x, schema: {'field': x, 'type': 'Nested', 'schema': f'{Naming.camelize(schema)}Schema'},  # noqa
                [_, 'nest', _, TAIL], lambda x, schema, t: merge_fields({'field': x, 'type': 'Nested', 'schema': f'{Naming.camelize(schema)}Schema'}, validate_attr(AFFIX, *t)),  # noqa
                [_, _, TAIL],         lambda x, y, t: merge_fields({'field': x, 'type': validate_type(y, TYPES)}, validate_attr(AFFIX, *t))  # noqa
    ) for attr in attrs]
