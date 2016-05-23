#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function
import random

from ipapy import IPA_TO_UNICODE
from ipapy import UNICODE_TO_IPA
from ipapy.mapper import Mapper

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

G2P_TOOLS = [
    u"phonetisaurus",
    u"sequitur"
]

FILTER_IPA_CHARS = [
    u"all",
    u"cv",
    u"cvs",
    u"cvsl",
    u"cvslw",
    u"cvslws",
]

class G2PTool(object):

    def __init__(self, lexicon, include_chars=None, mapper_name=None, train_size=0.9):
        self.lexicon = lexicon
        self.include_chars = include_chars
        self.mapper_name = mapper_name
        self.mapper = None
        self.train_symbol_set = set()
        self.test_symbol_set = set()
        self.train = []
        self.test = []
        self.generate_sets(train_size=train_size)

    def generate_sets(self, train_size):
        le_size = len(self.lexicon.cleaned_valid)
        if isinstance(train_size, int):
            if train_size > le_size:
                raise ValueError("The given train size (%d) is greater than the valid lexicon size (%d)." % (train_size, le_size))
            tr_size = train_size
        elif isinstance(train_size, float):
            tr_size = int(le_size * train_size)
        else:
            raise TypeError("Parameter train_size must be an int or a float.")
        # make a copy to avoid changing the original object
        l = self.lexicon.cleaned_valid
        random.shuffle(l)
        self.train = l[:tr_size]
        self.test = l[tr_size:]
        self._set_symbol_set()
        self._set_mapper()

    def _set_mapper(self):
        if self.mapper_name is None:
            self.mapper = Mapper()
            i = 1
            for c in self.symbol_set:
                self.mapper[c.descriptors] = u"%03d" % i
                i += 1

    def _filter_ipa_chars(self, lexicon_entry):
        if self.include_chars in [u"cv", u"cns_vwl", u"letters"]:
            s = lexicon_entry.cleaned_ipastring.cns_vwl
        elif self.include_chars in [u"cvs", u"cns_vwl_str"]:
            s = lexicon_entry.cleaned_ipastring.cns_vwl_str
        elif self.include_chars in [u"cvsl", u"cns_vwl_str_len"]:
            s = lexicon_entry.cleaned_ipastring.cns_vwl_str_len
        elif self.include_chars in [u"cvslw", u"cns_vwl_str_len_wb"]:
            s = lexicon_entry.cleaned_ipastring.cns_vwl_str_len_wb
        elif self.include_chars in [u"cvslws", u"cns_vwl_str_len_wb_sb"]:
            s = lexicon_entry.cleaned_ipastring.cns_vwl_str_len_wb_sb
        else:
            s = lexicon_entry.cleaned_ipastring
        return s

    def _set_symbol_set(self):
        def cs(entries):
            cs_chars = set()
            for e in entries:
                cs_chars |= set([c for c in self._filter_ipa_chars(e)])
            return cs_chars
        self.train_symbol_set = cs([e for e in self.train if e.cleaned_is_valid])
        self.test_symbol_set = cs([e for e in self.test if e.cleaned_is_valid])

    @property
    def train_size(self):
        return len(self.train)

    @property
    def test_size(self):
        return len(self.test)

    @property
    def train_symbol_set_size(self):
        return len(self.train_symbol_set)

    @property
    def test_symbol_set_size(self):
        return len(self.test_symbol_set)

    @property
    def symbol_set(self):
        return self.train_symbol_set | self.test_symbol_set

    @property
    def symbol_set_size(self):
        return len(self.symbol_set)

    def _format_g2p_input(self, entries):
        raise NotImplementedError("You must use a concrete subclass of G2PTool")

    def format_train(self):
        return self._format_g2p_input(self.train)

    def format_test(self):
        return self._format_g2p_input(self.test)

    def format_symbol_set(self):
        acc = []
        for k in self.mapper.ipa_descriptors:
            uni_char = IPA_TO_UNICODE[k]
            ipa_char = UNICODE_TO_IPA[uni_char]
            acc.append(u"%s\t%s\t%s" % (self.mapper[k], uni_char, ipa_char.name))
        return acc



class G2PPhonetisaurus(G2PTool):

    def _format_g2p_input(self, entries):
        acc = []
        for e in entries:
            word = e.word
            phones = [self.mapper[c.descriptors] for c in self._filter_ipa_chars(e)]
            acc.append(u"%s\t%s" % (word, u" ".join(phones)))
        return acc



class G2PSequitur(G2PTool):

    def _format_g2p_input(self, entries):
        acc = []
        for e in entries:
            word = e.word
            phones = [self.mapper[c.descriptors] for c in self._filter_ipa_chars(e)]
            acc.append(u"%s %s" % (word, u" ".join(phones)))
        return acc



