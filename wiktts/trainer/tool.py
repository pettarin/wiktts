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
import shutil

from ipapy import IPA_TO_UNICODE
from ipapy import UNICODE_TO_IPA

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

TOOLS = [
    u"phonetisaurus_08a",
    u"phonetisaurus_master",
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

    def format_words(self, train=False, test=True, sort=False):
        acc = []
        if train:
            acc.extend([e.cleaned_word_unicode for e in self.lexicon.train])
        if test:
            acc.extend([e.cleaned_word_unicode for e in self.lexicon.test])
        if sort:
            return sorted(acc)
        return acc

    def format_symbols(self, train=False, test=True, sort=True):
        acc = set()
        if train:
            acc |= set([u"%s\t%s\t%s" % (self.mapper[(p.canonical_representation,)], p.name, p.unicode_repr) for p in self.lexicon.train_symbol_set])
        if test:
            acc |= set([u"%s\t%s\t%s" % (self.mapper[(p.canonical_representation,)], p.name, p.unicode_repr) for p in self.lexicon.test_symbol_set])
        acc = list(acc)
        if sort:
            return sorted(acc)
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
        return [cls._format_script_contents(template, d)]

    @classmethod
    def _format_script_contents(cls, template, d):
        raise NotImplementedError("You must override this function in concrete subclasses.")



class ToolPhonetisaurusMaster(Tool):
    """
    Phonetisaurus as in current GitHub master
    (https://github.com/AdolfVonKleist/Phonetisaurus) with commit::

        commit 09651ed5f6e9040d6dd30070601ecccfad254df4
        Author: Josef Novak <joe@spitch.ch>
        Date:   Fri Mar 11 13:51:17 2016 +0000
        Update to optionally print out the state-symbols table

    Note: "./configure && make" terminates with errors because "make phonetisaurus-g2prnn" is broken,
    use instead::
    
        ./configure
        make phonetisaurus-align
        make phonetisaurus-arpa2wfst
        make rnnlm
        make phonetisaurus-g2pfst

    """

    DEFAULT_SCRIPT_NAME = u"run_phonetisaurus_master.sh"

    SCRIPT_TEMPLATE_FILE_PATH = u"templates/run_phonetisaurus_master.sh"

    COMPUTE_ER = u"templates/compute_er_phonetisaurus_master.py"

    DEFAULT_PARAMETERS = {
        "phonetisaurus_ngramorder": "8",
        "phonetisaurus_smoothing": "FixKN",
        "phonetisaurus_variants": "1",
    }

    def _format_g2p_input(self, entries):
        return [u"%s\t%s" % (e.cleaned_word_unicode, u" ".join(e.filtered_mapped_unicode)) for e in entries]

    @classmethod
    def _format_script_contents(cls, template, d):
        # copy COMPUTE_ER tool, derived from Phonetisaurus 0.8a,
        # to the destination directory,
        # since the tools on the current master seems to lack the "compute ER" feature
        src_path = os.path.join(os.path.dirname(__file__), cls.COMPUTE_ER)
        dest_path = os.path.join(d["output_dir_path"], os.path.basename(cls.COMPUTE_ER))
        shutil.copyfile(src_path, dest_path)
        return template.format(
            BASE=d["base"],
            NGRAMORDER=d["phonetisaurus_ngramorder"],
            SMOOTHING=d["phonetisaurus_smoothing"],
            VARIANTS=d["phonetisaurus_variants"],
            ERPY=dest_path,
        )



class ToolPhonetisaurus08a(Tool):
    """
    Phonetisaurus 0.8a (IS2013 paper) from
    https://code.google.com/archive/p/phonetisaurus/
    """

    DEFAULT_SCRIPT_NAME = u"run_phonetisaurus_08a.sh"

    SCRIPT_TEMPLATE_FILE_PATH = u"templates/run_phonetisaurus_08a.sh"

    DEFAULT_PARAMETERS = {
        "phonetisaurus_ngramorder": "8",
        "phonetisaurus_smoothing": "FixKN",
        "phonetisaurus_decoder": "fst_phi",
        "phonetisaurus_variants": "1",
    }

    def _format_g2p_input(self, entries):
        return [u"%s\t%s" % (e.cleaned_word_unicode, u" ".join(e.filtered_mapped_unicode)) for e in entries]

    @classmethod
    def _format_script_contents(cls, template, d):
        return template.format(
            BASE=d["base"],
            NGRAMORDER=d["phonetisaurus_ngramorder"],
            SMOOTHING=d["phonetisaurus_smoothing"],
            DECODER=d["phonetisaurus_decoder"],
            VARIANTS=d["phonetisaurus_variants"],
        )



class ToolSequitur(Tool):
    """
    Sequitur r1668-r3 (2016-04-25)
    """

    DEFAULT_SCRIPT_NAME = u"run_sequitur.sh"

    SCRIPT_TEMPLATE_FILE_PATH = u"templates/run_sequitur.sh"

    DEFAULT_PARAMETERS = {
        "sequitur_devel": "5",
        "sequitur_maxorder": "8",
        "sequitur_variants": "1"
    }

    def _format_g2p_input(self, entries):
        # NOTE sequitur does not allow spaces in word or phoneme symbol!
        # TODO warn the user
        return [u"%s %s" % (e.cleaned_word_unicode.replace(u" ", u""), u" ".join(e.filtered_mapped_unicode)) for e in entries]

    @classmethod
    def _format_script_contents(cls, template, d):
        return template.format(
            BASE=d["base"],
            DEVEL=d["sequitur_devel"],
            MAXORDER=d["sequitur_maxorder"],
            VARIANTS=d["sequitur_variants"]
        )



