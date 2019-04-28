from pampy import match, _, TAIL
from copier import copy

from horn.utils import Naming, get_proj_info, get_tpl_path


TPL_PATH = get_tpl_path('..', 'templates')


def run(opts):
    bindings = {
        'module': opts.get('<module>'),
        'fields': opts.get('<fields>'),
    }
