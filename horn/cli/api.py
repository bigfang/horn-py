from copier import copy

from horn.naming import Naming
from horn.path import get_tpl_path, get_location
from horn.tpl import get_proj_info

from . import service


TPL_PATH = get_tpl_path('..', 'templates')


def run(opts):
    service.run(opts)

    bindings = {
        'service': opts.get('<service>'),
        'module': opts.get('<module>'),
        'singular': Naming.underscore(opts.get('<module>')),
        'plural': opts.get('<table>')
    }
    bindings.update(get_proj_info())

    location = get_location(bindings) or TPL_PATH
    copy(f'{location}/gen', '.', data=bindings,
         exclude=['*/services/*', '*/models/*', '*/schemas/*', 'test/*'])
