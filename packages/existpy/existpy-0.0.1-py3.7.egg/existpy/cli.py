"""
existpy

Usage:
    existpy [packagename] [--summary]
    existpy -h | --help
    existpy -v | --version

Options:
    
    -h --help   Shows possible commands.
    -v --version    Shows current version of the package.

Help:
    For suggestions/problems and etc. visit the github reposityory https://github.com/monzita/existpy
"""
import sys
from docopt import docopt

from .command import exec_

VERSION = '0.0.1'

def main():
    global VERSION

    if len(sys.argv) < 2 or sys.argv[1] == '--summary':
        sys.argv.append('wrong format')
        docopt(__doc__, version=VERSION)
        return

    package_name = sys.argv[1]
    sys.argv.remove(package_name)

    options = docopt(__doc__, version=VERSION)

    exec_(package_name, with_summary=options['--summary'])