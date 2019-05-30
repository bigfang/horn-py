from docopt import docopt

import horn


def execli(input):
    opts = docopt(horn.__doc__, input.split())
    horn.Hub.run(opts)
    return opts
