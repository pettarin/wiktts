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

DEFAULT_IPA_REPLACEMENT_FILE_PATH = "data/unicleaner_ipa.dat"
#DEFAULT_WORD_REPLACEMENT_FILE_PATH = "data/unicleaner_word.dat"

class UniCleaner(object):

    def __init__(self, data_file_path, lowercase=False):
        self.data_file_path = data_file_path
        self.lowercase = lowercase
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
        if self.lowercase:
            s = s.lower()
        for (old, new) in self.replacements:
            s = s.replace(old, new)
        return s



class DefaultWordCleaner(UniCleaner):
    """
    TBW
    """
    def __init__(self, lowercase):
        super(DefaultWordCleaner, self).__init__(
            data_file_path=None,
            lowercase=lowercase
        )



class DefaultIPACleaner(UniCleaner):
    """
    TBW
    """
    def __init__(self):
        super(DefaultIPACleaner, self).__init__(
            data_file_path=os.path.join(os.path.dirname(__file__), DEFAULT_IPA_REPLACEMENT_FILE_PATH),
            lowercase=True
        )





