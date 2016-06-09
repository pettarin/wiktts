#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from wiktts.lexicon import Lexicon
from wiktts.lexicon import LexiconEntry

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class SequenceLexiconEntry(LexiconEntry):

    def __init__(self, raw_values, lowercase=False):
        self.word = None
        super(SequenceLexiconEntry, self).__init__(raw_values=raw_values, lowercase=lowercase)

    def _set_value(self, raw_values, lowercase):
        if len(raw_values) >= 2:
            self.word = raw_values[0]
            if lowercase:
                self.word = self.word.lower()
            self.value = raw_values[1].split(u" ")
            self.valid = True 

    @property
    def value_as_sequence(self):
        return self.value



class SequenceLexicon(Lexicon):
    """
    TBW
    """

    ENTRY_TYPE = SequenceLexiconEntry

    def __init__(self, entries=None, lowercase=False):
        self.include_valid = True
        self.include_invalid = False
        super(SequenceLexicon, self).__init__(entries=entries, lowercase=lowercase)

    def select_entries(self, include_valid=True, include_invalid=False):
        self.include_valid = include_valid
        self.include_invalid = include_invalid

    @property
    def selected_entries(self):
        entries = self.entries
        if (self.include_invalid) and (not self.include_valid):
            entries = [e for e in self.entries if not e.valid]
        elif (not self.include_invalid) and (self.include_valid):
            entries = [e for e in self.entries if e.valid]
        return entries

    def __iter__(self):
        for e in self.selected_entries:
            yield e

    @property
    def letters(self):
        letters = set()
        for e in self:
            letters |= e.letters
        return letters

    @property
    def symbols(self):
        symbols = set()
        for e in self:
            symbols |= e.symbols
        return symbols

    def pretty_print_stats(self):
        total = len(self)
        valid = len([e for e in self if e.valid])
        valid_perc = 100 * valid / total
        acc = []
        acc.append(u"Words")
        acc.append(u"  Total:   %d" % total)
        acc.append(u"  Valid:   %d (%0.3f%%)" % (valid, valid_perc))
        acc.append(u"  Invalid: %d (%0.3f%%)" % (total - valid, 100.0 - valid_perc))
        return u"\n".join(acc)



