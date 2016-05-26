#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function
import io
import os
import unicodedata
from ipapy import is_valid_ipa
from ipapy import remove_invalid_ipa_characters
from ipapy.compatibility import to_unicode_string
from ipapy.compatibility import unicode_to_hex
from ipapy.ipastring import IPAString

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

DEFAULT_TEMPLATE = {
    (True, True): u"{CWORDUNI}\t{CIPA}\t{CIPAUNIVALID}",
    (True, False): u"{CWORDUNI}\t{CIPA}",
    (False, True): u"{RWORDUNI}\t{RIPA}",

}

PLACEHOLDERS = [
    u"{RWORDUNI}",      # raw word (Unicode)
    u"{RIPAUNI}",       # raw Unicode string (Unicode)
    u"{RIPAUNIVALID}",  # raw IPA string is IPA valid (bool)
    u"{RIPA}",          # full repr of raw IPA string (Unicode)
    u"{RCV}",           # cns_vwl repr of raw IPA string (Unicode)
    u"{RCVP}",          # cns_vwl_pstr repr of raw IPA string (Unicode)
    u"{RCVS}",          # cns_vwl_str repr of raw IPA string (Unicode)
    u"{RCVPL}",         # cns_vwl_pstr_long repr of raw IPA string (Unicode)
    u"{RCVSL}",         # cns_vwl_str_len repr of raw IPA string (Unicode)
    u"{RCVSLW}",        # cns_vwl_str_len_wb repr of raw IPA string (Unicode)
    u"{RCVSLWS}",       # cns_vwl_str_len_wb_sb repr of raw IPA string (Unicode)
    u"{CWORDUNI}",      # cleaned word (Unicode)
    u"{CIPAUNI}",       # cleaned Unicode string (Unicode)
    u"{CIPAUNIVALID}",  # cleaned IPA string is IPA valid (bool)
    u"{CIPA}",          # full repr of cleaned+normalized IPA string (Unicode)
    u"{CCV}",           # cns_vwl repr of cleaned+normalized IPA string (Unicode)
    u"{CCVP}",          # cns_vwl_pstr repr of cleaned+normalized IPA string (Unicode)
    u"{CCVS}",          # cns_vwl_str repr of cleaned+normalized IPA string (Unicode)
    u"{CCVPL}",         # cns_vwl_pstr_long repr of cleaned+normalized IPA string (Unicode)
    u"{CCVSL}",         # cns_vwl_str_len repr of cleaned+normalized IPA string (Unicode)
    u"{CCVSLW}",        # cns_vwl_str_len_wb repr of cleaned+normalized IPA string (Unicode)
    u"{CCVSLWS}",       # cns_vwl_str_len_wb_sb repr of cleaned+normalized IPA string (Unicode)
]

class LexiconEntry(object):
    """
    TBW
    """

    def __init__(self, word_unicode, ipa_unicode, word_cleaner=None, ipa_cleaner=None):
        # store
        self.raw_word_unicode = word_unicode
        self.raw_ipa_unicode = ipa_unicode
        self.raw_ipa_is_valid = is_valid_ipa(self.raw_ipa_unicode)
        self.raw_ipastring = IPAString(
            unicode_string=self.raw_ipa_unicode,
            ignore=True,
            single_char_parsing=False
        )
        if (word_cleaner is None) or (ipa_cleaner is None):
            self.cleaned_word_unicode = word_unicode
            self.cleaned_ipa_unicode = ipa_unicode
            self.cleaned_ipa_is_valid = self.raw_ipa_is_valid
            self.cleaned_ipastring = self.raw_ipastring
        else:
            self.cleaned_word_unicode = word_cleaner.clean(word_unicode)
            self.cleaned_ipa_unicode = ipa_cleaner.clean(ipa_unicode)
            self.cleaned_ipa_is_valid = is_valid_ipa(self.cleaned_ipa_unicode)
            self.cleaned_ipastring = IPAString(
                unicode_string=self.cleaned_ipa_unicode,
                ignore=True,
                single_char_parsing=False
            )
        self.cleaned_ipa_valid_chars, self.cleaned_ipa_invalid_chars = remove_invalid_ipa_characters(
            unicode_string=self.cleaned_ipa_unicode,
            return_invalid=True,
            single_char_parsing=False
        )

    @property
    def canonical_unicode(self):
        return str(self.cleaned_ipastring)

    @property
    def raw_word_letters(self):
        return set(self.raw_word_unicode)

    @property
    def cleaned_word_letters(self):
        return set(self.cleaned_word_unicode)

    @property
    def raw_ipa_phones(self):
        return set(self.raw_ipastring.ipa_chars)

    @property
    def cleaned_ipa_phones(self):
        return set(self.cleaned_ipastring.ipa_chars)

    def format_entry(self, template, comment_string=u""):
        # TODO this is a bit ugly
        ret = template.format(
            RWORDUNI=self.raw_word_unicode,
            RIPAUNI=self.raw_ipa_unicode,
            RIPAUNIVALID=self.raw_ipa_is_valid,
            RIPA=self.raw_ipastring,
            RCV=self.raw_ipastring.cns_vwl,
            RCVP=self.raw_ipastring.cns_vwl_pstr,
            RCVS=self.raw_ipastring.cns_vwl_str,
            RCVPL=self.raw_ipastring.cns_vwl_pstr_long,
            RCVSL=self.raw_ipastring.cns_vwl_str_len,
            RCVSLW=self.raw_ipastring.cns_vwl_str_len_wb,
            RCVSLWS=self.raw_ipastring.cns_vwl_str_len_wb_sb,
            CWORDUNI=self.cleaned_word_unicode,
            CIPAUNI=self.cleaned_ipa_unicode,
            CIPAUNIVALID=self.cleaned_ipa_is_valid,
            CIPA=self.cleaned_ipastring,
            CCV=self.cleaned_ipastring.cns_vwl,
            CCVP=self.cleaned_ipastring.cns_vwl_pstr,
            CCVS=self.cleaned_ipastring.cns_vwl_str,
            CCVPL=self.cleaned_ipastring.cns_vwl_pstr_long,
            CCVSL=self.cleaned_ipastring.cns_vwl_str_len,
            CCVSLW=self.cleaned_ipastring.cns_vwl_str_len_wb,
            CCVSLWS=self.cleaned_ipastring.cns_vwl_str_len_wb_sb,
        )
        if self.cleaned_ipa_is_valid:
            return ret
        return comment_string + ret



class Lexicon(object):
    """
    TBW
    """

    def __init__(self, word_cleaner=None, ipa_cleaner=None):
        self.entries = []
        self.word_cleaner = word_cleaner
        self.ipa_cleaner = ipa_cleaner
        self.select_cleaned_ipa_valid = True
        self.select_cleaned_ipa_invalid = False

    def __len__(self):
        return len(self.entries)

    @property
    def raw_ipa_is_valid(self):
        return [e for e in self.entries if e.raw_ipa_is_valid]

    @property
    def cleaned_ipa_is_valid(self):
        return [e for e in self.entries if e.cleaned_ipa_is_valid]

    def __iter__(self):
        for e in self.entries:
            yield e

    def read_file(self, lexicon_file_path, comment=u"#", delimiter=u"\t", word_index=0, ipa_index=1):
        if (lexicon_file_path is None) or (not os.path.isfile(lexicon_file_path)):
            raise ValueError("The lexicon file path must exist. (Got '%s')" % lexicon_file_path)
        comment = to_unicode_string(comment)
        delimiter = to_unicode_string(delimiter)
        with io.open(lexicon_file_path, "r", encoding="utf-8") as lexicon_file:
            for line in lexicon_file:
                line = line.strip()
                if not line.startswith(comment):
                    acc = line.split(delimiter)
                    self.entries.append(LexiconEntry(
                        word_unicode=acc[word_index],
                        ipa_unicode=acc[ipa_index],
                        word_cleaner=self.word_cleaner,
                        ipa_cleaner=self.ipa_cleaner
                    ))

    def select_entries(self, ipa_valid=True, ipa_invalid=False):
        self.select_cleaned_ipa_valid = ipa_valid
        self.select_cleaned_ipa_invalid = ipa_invalid

    @property
    def selected_entries(self):
        if (self.select_cleaned_ipa_invalid) and (self.select_cleaned_ipa_valid):
            return self.entries
        elif (self.select_cleaned_ipa_invalid) and (not self.select_cleaned_ipa_valid):
            return [e for e in self.entries if not e.cleaned_ipa_is_valid]
        else:
            return [e for e in self.entries if e.cleaned_ipa_is_valid]

    @property
    def phones(self):
        phones = set()
        for e in self.selected_entries:
            phones |= e.cleaned_ipa_phones
        return phones

    @property
    def letters(self):
        letters = set()
        for e in self.selected_entries:
            letters |= e.cleaned_word_letters
        return letters

    def format_phones(self):
        return sorted([(u"%s\t%s (%s)" % (p.unicode_repr, p.name, unicode_to_hex(p.unicode_repr))) for p in self.phones])

    def format_letters(self):
        return sorted([(u"%s\t%s\t%s" % (l, unicode_to_hex(l), unicodedata.name(l, u"UNKNOWN"))) for l in self.letters])

    def format_lexicon(self, template=None, comment_invalid=False, comment=u"#"):
        # select template
        template = to_unicode_string(template) or DEFAULT_TEMPLATE[(self.select_cleaned_ipa_valid, self.select_cleaned_ipa_invalid)]
        # comment string to be prepended to invalid entries, if requested
        comment_string = comment if comment_invalid else u""
        # format data
        return [e.format_entry(template, comment_string) for e in self.selected_entries]



