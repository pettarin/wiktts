#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function
import io

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

__version__ = "0.1.0"
__status__ = "Development"

def write_file(formatted_data, output_file_path):
    with io.open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(u"\n".join(formatted_data))



