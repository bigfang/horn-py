import inflection
from pampy import match, _, TAIL
from copier import run_copy

from horn.path import TPL_PATH, get_location
from horn.tpl import get_proj_info
from . import model, schema


TYPE_MAP = {
    'integer': 'integer',
    'float': 'float',
    'boolean': 'boolean',
    'string': 'string',
    'date': 'date',
    'time': 'time',
    'datetime': 'datetime',
    'uuid': 'uuid',

    'decimal': 'decimal',
    'numeric': 'decimal',

    'ref': 'ref',
    'nest': 'nest',

    'array': 'list',
    'json': 'dict'
}


def run(opts):
    model.run(opts)
    sch_opts = opt_pipe(opts)
    schema.run(sch_opts)

    bindings = {
        'module': opts.get('<module>'),
        'singular': inflection.underscore(opts.get('<module>')),
        'plural': opts.get('<table>'),
        'table': opts.get('<table>'),
        'fields': opts.get('<fields>')
    }
    bindings.update(get_proj_info())

    location = get_location(bindings) or TPL_PATH
    run_copy(f'{location}/gen', '.', data=bindings, exclude=['*/models/*', '*/schemas/*', 'tests/*'])
    run_copy(f'{location}/gen/tests', './tests', data=bindings)


def opt_pipe(opts):
    o = prepare_opts(opts)
    p = slim_field(o)
    t = convert_type(p)
    s = ref_to_nest(t)
    return s


def prepare_opts(opts):
    """
    >>> opts = {'<module>': 'Blog'}
    >>> prepare_opts(opts)
    {'<module>': 'Blog', '--model': 'Blog'}
    """
    rv = opts.copy()
    rv.update({
        '--model': opts.get('<module>')
    })
    return rv


def slim_field(opts):
    opts['<fields>'] = [':'.join(match(
        field.split(':'),
        [_, _],        lambda x, y: [x, y],  # noqa: E241,E272
        [_, _, TAIL],  lambda x, y, t: [x, y] + drop_pair(t)  # noqa: E241,E272
    )) for field in opts['<fields>']]
    return opts


def drop_pair(attrs, key='default'):
    """
    >>> attrs = ['default', 'none', 'nonull', 'load']
    >>> drop_pair(attrs)
    ['nonull', 'load']
    """
    if key in attrs:
        idx = attrs.index(key)
        del attrs[idx:idx+2]    # noqa: E226
    return attrs


def convert_type(opts):
    opts['<fields>'] = [':'.join(match(
        field.split(':'),
        [_, _],        lambda x, y: [x, TYPE_MAP.get(y, 'string')],  # noqa: E241,E272
        [_, _, TAIL],  lambda x, y, t: [x, TYPE_MAP.get(y, 'string')] + t,  # noqa: E241,E272
    )) for field in opts['<fields>']]
    return opts


def ref_to_nest(opts):
    opts['<fields>'] = [':'.join(match(
        field.split(':'),
        [_, 'ref', _],       lambda x, y: [x, 'nest', inflection.singularize(y)],  # noqa: E241,E272
        [_, 'ref', _, TAIL], lambda x, y, t: [x, 'nest', inflection.singularize(y)] + t,  # noqa: E241,E272
        list,                lambda x: x  # noqa: E241,E272
    )) for field in opts['<fields>']]
    return opts
