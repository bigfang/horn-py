"""
Usage:
  horn new <folder> [--app=<app> --repo=<repo> --proj=<proj> --bare --pypi=<pypi>]
  horn gen (api | service) <service> <module> <table> <fields>...
  horn gen model <module> <table> <fields>...
  horn gen schema <module> <fields>...
  horn (-h | --help)
  horn --version

Options:
  -h --help         Show this screen.
  --version         Show version.
  --app=<app>       App name [default: app].
  --proj=<proj>     Project name.
  --pypi=<pypi>     Pypi domain [default: pypi.org].
  --bare            Bare project.

"""
from docopt import docopt
import impl


__version__ = '0.1.0'


ACTION_MAP = {
    'new': ['<folder>', '--app', '--proj', '--bare', '--pypi'],
    'api': ['<service>', '<module>', '<table>', '<fields>'],
    'service': ['<service>', '<module>', '<table>', '<fields>'],
    'model': ['<module>', '<table>', '<fields>'],
    'schema': ['<module>', '<fields>'],
}

ACTIONS = list(ACTION_MAP.keys())


class Hub(object):

    @classmethod
    def filter_opt(cls, action, params):
        keys = ACTION_MAP.get(action)
        return {k: v for k, v in params.items() if k in keys}

    @classmethod
    def run(cls, args):
        for action in ACTIONS:
            if args.get(action):
                opts = cls.filter_opt(action, args)
                getattr(impl, action).run(opts)
                break


def main():
    args = docopt(__doc__, version=f'Horn {__version__}')
    Hub.run(args)
    # print(args)


if __name__ == '__main__':
    main()
