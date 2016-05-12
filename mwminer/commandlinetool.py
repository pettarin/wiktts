#!/usr/bin/env python
# coding=utf-8

"""
Command line utility
"""

from __future__ import absolute_import
from __future__ import print_function
import argparse
import os
import sys

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class CommandLineTool(object):

    # overload in the actual subclass
    #
    AP_DESCRIPTION = "Generic Command Line Tool"
    AP_ARGUMENTS = [
        # implement in the actual 
        #
        # required args
        #{"name": "foo", "nargs": 1, "type": str, "default": "baz", "help": "Foo help"},
        #
        # optional args
        #{"name": "--bar", "nargs": "?", "type": str,, "default": "foofoofoo", "help": "Bar help"},
        #{"name": "--quiet", "action": "store_true", "help": "Do not output to stdout"},
    ]

    def __init__(self):
        self.parser = argparse.ArgumentParser(description=self.AP_DESCRIPTION)
        self.vargs = None
        for arg in self.AP_ARGUMENTS:
            if "action" in arg:
                self.parser.add_argument(arg["name"], action=arg["action"], help=arg["help"])
            else:
                self.parser.add_argument(arg["name"], nargs=arg["nargs"], type=arg["type"], default=arg["default"], help=arg["help"])

    def run(self):
        self.vargs = vars(self.parser.parse_args())
        self.actual_command()
        sys.exit(0)

    # overload this in your actual subclass
    def actual_command(self):
        print("This script does nothing. Invoke another .py")

    def error(self, message):
        print("ERROR: %s" % message)
        sys.exit(1)



def main():
    CommandLineTool().run()

if __name__ == "__main__":
    main()



