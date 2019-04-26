"""
Usage:
  horn new <proj> [--app=<app> --proj=<proj> --bare --pypi=<pypi>]
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


__version__ = '0.1.0'


def main():
    args = docopt(__doc__, version=f'Horn {__version__}')
    print(args)


if __name__ == '__main__':
    main()
