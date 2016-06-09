#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ipapy import is_valid_ipa
from ipapy.ipastring import IPAString

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class WordPronunciationPair(object):

    def __init__(self, word_unicode, pron_unicode=None, pron_ipastring=None):
        self.word_unicode = word_unicode
        if pron_ipastring is None:
            self.pron_unicode = pron_unicode
            self.pron_unicode_is_valid = is_valid_ipa(self.pron_unicode)
            self.pron_ipastring = IPAString(
                unicode_string=self.pron_unicode,
                ignore=True,
                single_char_parsing=False
            )
        else:
            self.pron_ipastring = pron_ipastring
            self.pron_unicode = pron_ipastring.__unicode__()
            self.pron_unicode_is_valid = True

    @property
    def letters(self):
        return set(self.word_unicode)

    @property
    def phones(self):
        return set(self.pron_ipastring.ipa_chars)



