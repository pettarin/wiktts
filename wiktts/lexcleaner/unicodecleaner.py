#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function
import os

from ipapy.data import load_data_file

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class UnicodeCleaner(object):

    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.replacements = self._load_replacements()
        
    def _load_replacements(self):
        acc = []     
        if self.data_file_path is not None:
            for (old, new) in load_data_file(
                file_path=self.data_file_path,
                file_path_is_relative=False,
                comment_string=u"#",
                field_separator=u",",
                line_format="UU"
            ):
                old = old[0]
                new = u"" if ((new is None) or (len(new) == 0)) else new[0]
                acc.append((old, new))
        return acc

    def clean(self, s):
        for (old, new) in self.replacements:
            s = s.replace(old, new)
        return s



