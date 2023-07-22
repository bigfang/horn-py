"""\t\t\033[1;33mHorn: A Flask scaffolding tool.\033[0m

Usage:
  horn new <target> [--app=<app> --proj=<proj> --pypi=<pypi> --bare]
  horn new <target> <from> [<checkout>] [--json=<json>] [-f=PATH | --file=PATH]
  horn gen api <module> <table> <fields>...
  horn gen model <module> <table> <fields>...
  horn gen schema <module> (<fields>... | --model=<model> | <fields>...  --model=<model>)
  horn -h | --help
  horn --version

Options:
  --app=<app>               App name [default: app].
  --proj=<proj>             Project name.
  --pypi=<pypi>             Pypi domain.
  --bare                    Bare project.

  --json=<json>             Json string [default: {}].
  -f=PATH, --file=PATH      Json file PATH.

  --model=<model>           Schema baseed on model.

  -h, --help                Show this screen.
  --version                 Show version.

Examples:
  horn \033[34mnew\033[0m tmp/foo_bar \033[32m--app\033[0m foobar \033[32m--proj\033[0m FooBar
  horn \033[34mnew\033[0m tmp/foo_bar https://github.com/bigfang/drf-starter.git \033[32m--json\033[0m '{"app":"someapp"}'
  horn \033[34mgen api\033[0m Post posts \033[36mtitle:string:uniq content:text:nonull author:ref:users\033[0m
  horn \033[34mgen model\033[0m Post posts \033[36mtitle:string:uniq:index content:string:nonull author:ref:users:nonull\033[0m
  horn \033[34mgen schema\033[0m Post \033[36mtitle:string content:string author:nest:user\033[0m

Notes:
  Model attrs:  uniq => unique=True, nonull => nullable=False,
                index => index=True, default:val => default=val
  Schema attrs: dump => dump_only, load => load_only, exclude => exclude,
                required => required=True, none => allow_none=True

"""
from docopt import docopt

from . import cli

__all__ = ['main', '__version__']


__version__ = '0.6.4'

ACTION_MAP = {
    'new': ['<target>', '--app', '--proj', '--bare', '--pypi', '<from>', '<checkout>', '--json', '--file'],
    'api': ['<module>', '<table>', '<fields>'],
    'model': ['<module>', '<table>', '<fields>'],
    'schema': ['<module>', '<fields>', '--model'],
}

ACTIONS = list(ACTION_MAP.keys())


class Hub(object):

    @classmethod
    def filter_opts(cls, action, params):
        keys = ACTION_MAP.get(action)
        return {k: v for k, v in params.items() if k in keys}

    @classmethod
    def run(cls, args):
        for action in ACTIONS:
            if args.get(action):
                opts = cls.filter_opts(action, args)
                cls.dispatch_action(action, opts)
                break

    @classmethod
    def dispatch_action(cls, action, opts):
        if action == 'new':
            if opts.get('<from>'):
                cli.repo.run(opts)
            else:
                cli.new.run(opts)
        else:
            getattr(cli, action).run(opts)


def main():
    args = docopt(__doc__, version=f'Horn {__version__}')
    Hub.run(args)
