# type: ignore
"""IDOM

Custom install configuration options

Usage:
  htm-pyx [register | deregister | registered | location]
"""
import os
from distutils.sysconfig import get_python_lib

import htm_pyx
from docopt import docopt


PTH_FILE = os.path.join(get_python_lib(), "htm_pyx.pth")


def main():
    arguments = docopt(__doc__, version=htm_pyx.__version__)
    for output in execute(arguments):
        print(output)


def execute(arguments):
    return map(str, _execute(arguments))


def _execute(arguments):
    if arguments["register"]:
        if os.path.exists(PTH_FILE):
            yield f"already registered: '{PTH_FILE}'"
        else:
            with open(PTH_FILE, "w+") as f:
                f.write("import htm_pyx\n")
    elif arguments["deregister"]:
        if not os.path.exists(PTH_FILE):
            yield f"already deregistered: '{PTH_FILE}'"
        else:
            os.remove(PTH_FILE)
    elif arguments["registered"]:
        yield os.path.exists(PTH_FILE)
    elif arguments["location"]:
        yield PTH_FILE


if __name__ == "__main__":
    main()
