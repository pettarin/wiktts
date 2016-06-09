#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function
import os

from wiktts.lexcleaner.unicodecleaner import UnicodeCleaner

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class PronunciationCleaner(UnicodeCleaner):
    """
    TBW
    """

    IPA_REPLACEMENT_FILE_PATH = "data/pronunciationcleaner.dat"

    def __init__(self):
        super(PronunciationCleaner, self).__init__(
            data_file_path=os.path.join(os.path.dirname(__file__), self.IPA_REPLACEMENT_FILE_PATH)
        )





