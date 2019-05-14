from pampy import match, _, TAIL
from copier import copy

from horn.naming import Naming
from horn.path import TPL_PATH, get_location
from horn.tpl import get_proj_info, validate_opts
from . import model, schema


def run(opts):
    model.run(opts)
    sch_opts = ref_to_nest(opts)
    schema.run(sch_opts)

    validate_opts(opts)

    bindings = {
        'service': opts.get('<service>'),
        'module': opts.get('<module>'),
        'mod': Naming.underscore(opts.get('<module>')),
        'singular': Naming.underscore(opts.get('<service>')),
        'table': opts.get('<table>'),
        'fields': opts.get('<fields>')
    }
    bindings.update(get_proj_info())

    location = get_location(bindings) or TPL_PATH
    copy(f'{location}/gen', '.', data=bindings,
         exclude=['*/models/*', '*/schemas/*', '*/views/*', 'test/*'])


def ref_to_nest(opts):
    rv = opts.copy()
    rv.update({
        '--model': opts.get('<module>')
    })
    fields = rv.get('<fields>')
    rv['<fields>'] = [':'.join(match(
        field.split(':'),
        [_, 'ref', _],       lambda x, y: [x, 'nest', Naming.singular(y)],  # noqa
        [_, 'ref', _, TAIL], lambda x, y, t: [x, 'nest', Naming.singular(y)] + drop_pair(t),  # noqa
        list,                lambda x: drop_pair(x)  # noqa
    )) for field in fields]
    return rv


def drop_pair(attrs, key='default'):
    if key in attrs:
        idx = attrs.index(key)
        del attrs[idx:idx+2]    # noqa: E226
    return attrs
