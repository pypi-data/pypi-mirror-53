#!/usr/bin/env python
from __future__ import division

"""gethelp.py: get help from a command-line script
"""

## Copyright 2011 Michael M. Hoffman <mmh1@uw.edu>

from __future__ import absolute_import
from six.moves.configparser import RawConfigParser
from cStringIO import StringIO
import sys

sys.path.insert(0, "..")
from setup import py3_entry_points, py2_entry_points
from segtools.version import __version__

def gethelp(scriptname):
    config = RawConfigParser()
    config.readfp(StringIO(py2_entry_points + py3_entry_points))

    entry = config.get("console_scripts", scriptname).split()[0]
    module_name, _, func_name = entry.partition(":")

    # __import__(module_name) usually returns the top-level package module only
    # so get our module out of sys.modules instead
    __import__(module_name)
    module = sys.modules[module_name]

    sys.argv[0] = scriptname
    getattr(module, func_name)(["--help"])

def parse_options(args):
    from optparse import OptionParser

    usage = "%prog [OPTION]... SCRIPTNAME"
    version = "%%prog %s" % __version__
    parser = OptionParser(usage=usage, version=version)

    options, args = parser.parse_args(args)

    if not len(args) == 1:
        parser.error("incorrect number of arguments")

    return options, args

def main(args=sys.argv[1:]):
    options, args = parse_options(args)

    return gethelp(*args)

if __name__ == "__main__":
    sys.exit(main())
