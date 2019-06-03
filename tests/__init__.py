import os

from docopt import docopt

import horn


def execli(params, cwd=None):
    if cwd:
        os.chdir(cwd)
    opts = docopt(horn.__doc__, params.split())
    horn.Hub.run(opts)
    return opts
