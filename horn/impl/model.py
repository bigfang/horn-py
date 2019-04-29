from pampy import match, _, TAIL
from copier import copy

from horn.utils import (clone, Naming, get_proj_info, get_tpl_path,
                        merge_fields, validate_type, validate_attr)


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
}

AFFIX = ('uniq', 'nonull', 'index')


def run(opts):
    bindings = {
        'module': opts.get('<module>'),
        'singular': Naming.underscore(opts.get('<module>')),
        'table': opts.get('<table>'),
        'fields': parse_fields(opts.get('<fields>'))
    }

    bindings.update(get_proj_info())

    location = TPL_PATH
    if bindings.get('repo'):
        location = clone(bindings.get('repo'), bindings.get('checkout'))
    copy(f'{location}/gen', '.', data=bindings,
         exclude=['*/services/*', '*/schemas/*', '*/views/*', 'test/*'])


def resolve_assign(ftype, default):
    rv = default
    if default == 'none':
        rv = 'None'
    elif ftype in ['integer', 'float', 'decimal']:
        pass
    elif ftype in ['boolen']:
        if default in ['true', 'false']:
            rv = Naming.camelize(default)
        else:
            print(f'Boolean field error: {default}')
    else:
        rv = f"'{rv}'"
    return rv


def parse_fields(fields):
    attrs = [f.split(':') for f in fields]
    return [match(
        attr,
        [_, _],              lambda x, y: {'field': x, 'type': validate_type(y, TYPES)},  # noqa
        [_, 'ref', _],       lambda x, table: {'field': x, 'type': validate_type('ref', TYPES), 'table': table},  # noqa
        [_, 'ref', _, TAIL], lambda x, table, t: merge_fields({'field': x, 'type': validate_type('ref', TYPES), 'table': table}, validate_attr(AFFIX,*t)),  # noqa
        [_, _, 'default', _],       lambda x, y, val: {'field': x, 'type': validate_type(y, TYPES), 'default': resolve_assign(y, val)},  # noqa
        [_, _, 'default', _, TAIL], lambda x, y, val, t: merge_fields({'field': x, 'type': validate_type(y, TYPES), 'default': resolve_assign(y, val)}, validate_attr(AFFIX, *t)),  # noqa
        [_, _, TAIL],        lambda x, y, t: merge_fields({'field': x, 'type': validate_type(y, TYPES)}, validate_attr(AFFIX, *t))  # noqa
    ) for attr in attrs]
