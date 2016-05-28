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

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

TOOLS = [
    u"phonetisaurus",
    u"sequitur"
]

class Tool(object):

    def __init__(self, lexicon, mapper):
        self.lexicon = lexicon
        self.mapper = mapper

    def _format_g2p_input(self, entries):
        raise NotImplementedError("You must use a concrete subclass of Tool")

    def format_train(self):
        return self._format_g2p_input(self.lexicon.train)

    def format_test(self):
        return self._format_g2p_input(self.lexicon.test)

    def format_symbol_set(self):
        acc = []
        for k in self.mapper.ipa_descriptors:
            uni_char = IPA_TO_UNICODE[k[0]]
            ipa_char = UNICODE_TO_IPA[uni_char]
            acc.append(u"%s\t%s (%s)" % (self.mapper[k], ipa_char.name, uni_char))
        return sorted(acc)

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
            word = e.cleaned_word_unicode
            phones = e.filtered_mapped_unicode
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
            word = e.cleaned_word_unicode.replace(u" ", u"")
            phones = e.filtered_mapped_unicode
            acc.append(u"%s %s" % (word, u" ".join(phones)))
        return acc

    @classmethod
    def _format_script_contents(cls, template, d):
        return template.format(
            BASE=d["base"],
            DEVEL=d["sequitur_devel"],
            MAXLEVEL=d["sequitur_maxlevel"]
        )



