import inflection
from pampy import match, _, TAIL
from copier import run_copy

from horn.path import TPL_PATH, get_location
from horn.tpl import get_proj_info, merge_fields, validate_type, validate_attr, validate_opts


TYPES = {
    'integer': 'Integer',
    'float': 'Float',
    'numeric': 'Numeric',
    'boolean': 'Boolean',
    'string': 'String',
    'text': 'Text',
    'date': 'Date',
    'time': 'Time',
    'datetime': 'DateTime',
    'uuid': 'UUID',
    'json': 'JSON',
    'array': 'ARRAY',

    'decimal': 'Numeric',
    'ref': 'reference',
}

AFFIXES = ('uniq', 'nonull', 'index')


def run(opts):
    validate_opts(opts)

    bindings = {
        'module': opts.get('<module>'),
        'singular': inflection.underscore(opts.get('<module>')),
        'table': inflection.underscore(opts.get('<table>')),
        'fields': parse_fields(opts.get('<fields>')),
        'has_ref': any([':ref:' in f for f in opts['<fields>']])
    }
    bindings.update(get_proj_info())

    location = get_location(bindings) or TPL_PATH
    run_copy(f'{location}/gen', '.', data=bindings, exclude=['*/schemas/*', '*/views/*', 'tests/*'])


def resolve_assign(ftype, default):
    """
    >>> resolve_assign('xxx', 'none')
    'None'
    >>> resolve_assign('ref', '100')
    100
    >>> try:
    ...     resolve_assign('ref', 'apple')
    ... except:
    ...     pass
    Error: Default value must be an integer
    >>> resolve_assign('float', '99.9')
    '99.9'
    >>> resolve_assign('boolean', 'false')
    'False'
    >>> try:
    ...     resolve_assign('boolean', 'apple')
    ... except:
    ...     pass
    Error: Boolean field error, apple
    >>> resolve_assign('ooo', 'elixir')
    "'elixir'"
    """
    rv = default
    if default == 'none':
        rv = 'None'
    elif ftype == 'ref':
        try:
            rv = int(default)
        except ValueError:
            print('Error: Default value must be an integer')
            exit(1)
    elif ftype in ['integer', 'float', 'numeric']:
        pass
    elif ftype in ['boolean']:
        if default in ['true', 'false']:
            rv = inflection.camelize(default)
        else:
            print(f'Error: Boolean field error, {default}')
            exit(1)
    else:
        rv = f"'{rv}'"
    return rv


def parse_fields(fields):
    from .schema import AFFIXES as SCH_AFFIXES

    attrs = [f.split(':') for f in fields]
    return [match(
        attr,
        [_, 'default', _, 'ref', _, TAIL], lambda x, val, tab, t: merge_fields({'field': x, 'cam_field': inflection.camelize(x), 'type': validate_type('ref', TYPES), 'table': tab, 'default': resolve_assign('ref', val)}, validate_attr(t, AFFIXES, SCH_AFFIXES)),  # noqa: E241,E272
        [_, 'ref', _, 'default', _, TAIL], lambda x, tab, val, t: merge_fields({'field': x, 'cam_field': inflection.camelize(x), 'type': validate_type('ref', TYPES), 'table': tab, 'default': resolve_assign('ref', val)}, validate_attr(t, AFFIXES, SCH_AFFIXES)),  # noqa: E241,E272
        [_, 'ref', _, TAIL], lambda x, tab, t: merge_fields({'field': x, 'cam_field': inflection.camelize(x), 'type': validate_type('ref', TYPES), 'table': tab}, validate_attr(t, AFFIXES, SCH_AFFIXES)),  # noqa: E241,E272
        [_, _, 'default', _, TAIL], lambda x, y, val, t: merge_fields({'field': x, 'type': validate_type(y, TYPES), 'default': resolve_assign(y, val)}, validate_attr(t, AFFIXES, SCH_AFFIXES)),  # noqa: E241,E272
        [_, _, TAIL],        lambda x, y, t: merge_fields({'field': x, 'type': validate_type(y, TYPES)}, validate_attr(t, AFFIXES, SCH_AFFIXES))  # noqa: E241,E272
    ) for attr in attrs]
