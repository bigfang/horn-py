import os

from docopt import docopt

import horn


def execli(params, cwd=None):
    if cwd:
        os.chdir(str(cwd))
    opts = docopt(horn.__doc__, params.split())
    horn.Hub.run(opts)
    return opts


def lint(path):
    out = os.popen(f'flake8 {str(path)}').read()
    print(out)
    return False if out else True
