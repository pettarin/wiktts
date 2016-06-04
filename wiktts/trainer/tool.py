#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function
import io
import os
import shutil

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class Tool(object):

    TEMPLATES_DIRECTORY_PATH = u"templates"

    def __init__(self, lexicon, mapper):
        self.lexicon = lexicon
        self.mapper = mapper

    def _format_g2p_input(self, entries):
        raise NotImplementedError(u"You must use a concrete subclass of Tool")

    def format_train(self):
        return self._format_g2p_input(self.lexicon.train)

    def format_test(self):
        return self._format_g2p_input(self.lexicon.test)

    def format_tab(self, train=False, test=True, sort=False):
        def format_entries(entries):
            return [u"%s\t%s" % (e.cleaned_word_unicode, u" ".join(e.filtered_mapped_unicode)) for e in entries]
        acc = []
        if train:
            acc.extend(format_entries(self.lexicon.train))
        if test:
            acc.extend(format_entries(self.lexicon.test))
        if sort:
            return sorted(acc)
        return acc

    def format_words(self, train=False, test=True, sort=False):
        def format_list(where):
            return [e.cleaned_word_unicode for e in where]
        acc = []
        if train:
            acc.extend(format_list(self.lexicon.train))
        if test:
            acc.extend(format_list(self.lexicon.test))
        if sort:
            return sorted(acc)
        return acc

    def format_symbols(self, train=False, test=True, sort=True):
        def format_set(where):
            return set([u"%s\t%s\t%s" % (self.mapper[(p.canonical_representation,)], p.name, p.unicode_repr) for p in where])
        acc = set()
        if train:
            acc |= format_set(self.lexicon.train_symbol_set)
        if test:
            acc |= format_set(self.lexicon.test_symbol_set)
        acc = list(acc)
        if sort:
            return sorted(acc)
        return acc

    @classmethod
    def format_script(cls, parameters):
        template_file_path = os.path.join(
            os.path.dirname(__file__),
            cls.TEMPLATES_DIRECTORY_PATH,
            cls.SCRIPT_FILE_NAME
        )
        with io.open(template_file_path, "r", encoding="utf-8") as template_file:
            template = template_file.read()
        if u"base" not in parameters:
            raise ValueError(u"The parameters dictionary does not contain a 'base' key.")
        d = dict()
        d.update(cls.DEFAULT_PARAMETERS)
        d.update(parameters)
        return [cls._format_script_contents(template, d)]

    @classmethod
    def _format_script_contents(cls, template, d):
        raise NotImplementedError(u"You must override this function in concrete subclasses.")



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

    COMPUTE_ER = u"compute_er_phonetisaurus_master.py"
    
    SCRIPT_FILE_NAME = u"run_phonetisaurus_master.sh"

    DEFAULT_PARAMETERS = {
        u"ngramorder": u"8",
        u"smoothing": u"FixKN",
        u"variants": u"1",
    }

    def _format_g2p_input(self, entries):
        return [u"%s\t%s" % (e.cleaned_word_unicode, u" ".join(e.filtered_mapped_unicode)) for e in entries]

    @classmethod
    def _format_script_contents(cls, template, d):
        # copy COMPUTE_ER tool, derived from Phonetisaurus 0.8a,
        # to the destination directory,
        # since the tools on the current master seems to lack the "compute ER" feature
        src_path = os.path.join(
            os.path.dirname(__file__),
            cls.TEMPLATES_DIRECTORY_PATH,
            cls.COMPUTE_ER
        )
        dest_path = os.path.abspath(os.path.join(d["output_dir_path"], cls.COMPUTE_ER))
        shutil.copyfile(src_path, dest_path)
        return template.format(
            BASE=d["base"],
            NGRAMORDER=d["ngramorder"],
            SMOOTHING=d["smoothing"],
            VARIANTS=d["variants"],
            ERPY=dest_path,
        )



class ToolPhonetisaurus08a(Tool):
    """
    Phonetisaurus 0.8a (IS2013 paper) from
    https://code.google.com/archive/p/phonetisaurus/
    """

    SCRIPT_FILE_NAME = u"run_phonetisaurus_08a.sh"

    DEFAULT_PARAMETERS = {
        u"ngramorder": u"8",
        u"smoothing": u"FixKN",
        u"decoder": u"fst_phi",
        u"variants": u"1",
    }

    def _format_g2p_input(self, entries):
        return [u"%s\t%s" % (e.cleaned_word_unicode, u" ".join(e.filtered_mapped_unicode)) for e in entries]

    @classmethod
    def _format_script_contents(cls, template, d):
        return template.format(
            BASE=d["base"],
            NGRAMORDER=d["ngramorder"],
            SMOOTHING=d["smoothing"],
            DECODER=d["decoder"],
            VARIANTS=d["variants"],
        )



class ToolSequitur(Tool):
    """
    Sequitur r1668-r3 (2016-04-25)
    """

    SCRIPT_FILE_NAME = u"run_sequitur.sh"

    DEFAULT_PARAMETERS = {
        u"devel": u"5",
        u"maxorder": u"8",
        u"variants": u"1"
    }

    def _format_g2p_input(self, entries):
        # NOTE sequitur does not allow spaces in word or phoneme symbol!
        # TODO warn the user
        return [u"%s %s" % (e.cleaned_word_unicode.replace(u" ", u""), u" ".join(e.filtered_mapped_unicode)) for e in entries]

    @classmethod
    def _format_script_contents(cls, template, d):
        return template.format(
            BASE=d["base"],
            DEVEL=d["devel"],
            MAXORDER=d["maxorder"],
            VARIANTS=d["variants"]
        )



TOOLS = {
    u"phonetisaurus_08a": ToolPhonetisaurus08a,
    u"phonetisaurus_master": ToolPhonetisaurusMaster,
    u"sequitur": ToolSequitur,
}



