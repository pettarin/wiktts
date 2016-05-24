#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function
import io
import os
import random

from ipapy import IPA_TO_UNICODE
from ipapy import UNICODE_TO_IPA
from ipapy.mapper import Mapper

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

TOOLS = [
    u"phonetisaurus",
    u"sequitur"
]

FILTER_IPA_CHARS = [
    u"all",
    u"cv",
    u"cvp",
    u"cvs",
    u"cvpl",
    u"cvsl",
    u"cvslw",
    u"cvslws",
]

class Tool(object):

    def __init__(self, lexicon, include_chars=None, mapper_name=None, train_size=0.9):
        self.lexicon = lexicon
        self.include_chars = include_chars
        self.filtered_lexicon_entries = []
        self.mapper_name = mapper_name
        self.mapper = None
        self.train_symbol_set = set()
        self.test_symbol_set = set()
        self.train = []
        self.test = []
        self._filter_lexicon_entries()
        self.generate_sets(train_size=train_size)

    def _filter_lexicon_entries(self):
        valid = self.lexicon.cleaned_valid
        if self.include_chars in [u"cv", u"cns_vwl", u"letters"]:
            self.filtered_lexicon_entries = [(e.cleaned_word_unicode, e.cleaned_ipastring.cns_vwl) for e in valid]
        elif self.include_chars in [u"cvp", u"cns_vwl_pstr"]:
            self.filtered_lexicon_entries = [(e.cleaned_word_unicode, e.cleaned_ipastring.cns_vwl_pstr) for e in valid]
        elif self.include_chars in [u"cvs", u"cns_vwl_str"]:
            self.filtered_lexicon_entries = [(e.cleaned_word_unicode, e.cleaned_ipastring.cns_vwl_str) for e in valid]
        elif self.include_chars in [u"cvpl", u"cns_vwl_pstr_long"]:
            self.filtered_lexicon_entries = [(e.cleaned_word_unicode, e.cleaned_ipastring.cns_vwl_pstr_long) for e in valid]
        elif self.include_chars in [u"cvsl", u"cns_vwl_str_len"]:
            self.filtered_lexicon_entries = [(e.cleaned_word_unicode, e.cleaned_ipastring.cns_vwl_str_len) for e in valid]
        elif self.include_chars in [u"cvslw", u"cns_vwl_str_len_wb"]:
            self.filtered_lexicon_entries = [(e.cleaned_word_unicode, e.cleaned_ipastring.cns_vwl_str_len_wb) for e in valid]
        elif self.include_chars in [u"cvslws", u"cns_vwl_str_len_wb_sb"]:
            self.filtered_lexicon_entries = [(e.cleaned_word_unicode, e.cleaned_ipastring.cns_vwl_str_len_wb_sb) for e in valid]
        else:
            self.filtered_lexicon_entries = [(e.cleaned_word_unicode, e.cleaned_ipastring) for e in valid]
        
    def generate_sets(self, train_size):
        le_size = len(self.filtered_lexicon_entries)
        if isinstance(train_size, int):
            if train_size > le_size:
                raise ValueError("The given train size (%d) is greater than the valid lexicon size (%d)." % (train_size, le_size))
            tr_size = train_size
        elif isinstance(train_size, float):
            tr_size = int(le_size * train_size)
        else:
            raise TypeError("Parameter train_size must be an int or a float.")
        # make a copy to avoid changing the original object
        random.shuffle(self.filtered_lexicon_entries)
        self.train = self.filtered_lexicon_entries[:tr_size]
        self.test = self.filtered_lexicon_entries[tr_size:]
        self._set_symbol_set()
        self._set_mapper()

    def _set_symbol_set(self):
        def cs(entries):
            cs_chars = set()
            for e in entries:
                cs_chars |= set([c for c in e[1]])
            return cs_chars
        self.train_symbol_set = cs(self.train)
        self.test_symbol_set = cs(self.test)

    def _set_mapper(self):
        if self.mapper_name is None:
            self.mapper = Mapper()
            i = 1
            for c in self.symbol_set:
                self.mapper[c.descriptors] = u"%03d" % i
                i += 1

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
        raise NotImplementedError("You must use a concrete subclass of Tool")

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

    @classmethod
    def format_script(cls, parameters):
        template_file_path = os.path.join(os.path.dirname(__file__), cls.SCRIPT_TEMPLATE_FILE_PATH)
        with io.open(template_file_path, "r", encoding="utf-8") as template_file:
            template = template_file.read()
        if u"base" not in parameters:
            raise ValueError("The parameters dictionary does not contain a 'base' key.")
        d = dict()
        d.update(cls.DEFAULT_PARAMETERS)
        d.update(parameters)
        return ([cls._format_script_contents(template, d)], cls.DEFAULT_SCRIPT_NAME)

    @classmethod
    def _format_script_contents(cls, template, d):
        raise NotImplementedError("You must override this function in concrete subclasses.")



class ToolPhonetisaurus(Tool):

    DEFAULT_SCRIPT_NAME = u"run_phonetisaurus.sh"

    SCRIPT_TEMPLATE_FILE_PATH = u"templates/run_phonetisaurus.sh"

    DEFAULT_PARAMETERS = {
        "phonetisaurus_ngramorder": "8",
        "phonetisaurus_smoothing": "FixKN",
        "phonetisaurus_decoder": "fst_phi",
    }

    def _format_g2p_input(self, entries):
        acc = []
        for e in entries:
            word = e[0]
            phones = [self.mapper[c.descriptors] for c in e[1]]
            acc.append(u"%s\t%s" % (word, u" ".join(phones)))
        return acc

    @classmethod
    def _format_script_contents(cls, template, d):
        return template.format(
            BASE=d["base"],
            NGRAMORDER=d["phonetisaurus_ngramorder"],
            SMOOTHING=d["phonetisaurus_smoothing"],
            DECODER=d["phonetisaurus_decoder"]
        )



class ToolSequitur(Tool):

    DEFAULT_SCRIPT_NAME = u"run_sequitur.sh"

    SCRIPT_TEMPLATE_FILE_PATH = u"templates/run_sequitur.sh"

    DEFAULT_PARAMETERS = {
        "sequitur_devel": "5",
        "sequitur_maxlevel": "8",
    }

    def _format_g2p_input(self, entries):
        acc = []
        for e in entries:
            # NOTE sequitur does not allow spaces in word or phoneme symbol!
            # TODO warn the user
            word = e[0].replace(u" ", u"")
            phones = [self.mapper[c.descriptors] for c in e[1]]
            acc.append(u"%s %s" % (word, u" ".join(phones)))
        return acc

    @classmethod
    def _format_script_contents(cls, template, d):
        return template.format(
            BASE=d["base"],
            DEVEL=d["sequitur_devel"],
            MAXLEVEL=d["sequitur_maxlevel"]
        )



