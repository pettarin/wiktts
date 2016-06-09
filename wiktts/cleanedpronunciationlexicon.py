#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from wiktts.pronunciationlexicon import PronunciationLexicon
from wiktts.pronunciationlexicon import PronunciationLexiconEntry
from wiktts.wordpronunciationpair import WordPronunciationPair

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class CleanedPronunciationLexiconEntry(PronunciationLexiconEntry):

    def __init__(self, raw_values, lowercase=False):
        self.cleaned = None
        super(CleanedPronunciationLexiconEntry, self).__init__(raw_values=raw_values, lowercase=lowercase)

    def apply_cleaner(self, word_cleaner, pron_cleaner):
        cleaned_word_unicode = self.raw.word_unicode if word_cleaner is None else word_cleaner.clean(self.raw.word_unicode)
        cleaned_pron_unicode = self.raw.pron_unicode if pron_cleaner is None else pron_cleaner.clean(self.raw.pron_unicode)
        self.cleaned = WordPronunciationPair(
            word_unicode=cleaned_word_unicode,
            pron_unicode=cleaned_pron_unicode
        )
        self.filtered = self.cleaned
        self.valid = self.cleaned.pron_unicode_is_valid
        self.value = self.cleaned.pron_ipastring

    def filter_chars(self, chars):
        self.filtered = WordPronunciationPair(
            word_unicode=self.cleaned.word_unicode,
            pron_ipastring=self.cleaned.pron_ipastring.filter_chars(chars=chars)
        )
        self.value = self.filtered.pron_ipastring

    def _format_template(self, template):
        return template.format(
            WORDUNI=self.raw.word_unicode,
            PRONUNI=self.raw.pron_unicode,
            PRONUNIVALID=self.raw.pron_unicode_is_valid,
            IPA=self.raw.pron_ipastring,
            CWORDUNI=self.cleaned.word_unicode,
            CPRONUNI=self.cleaned.pron_unicode,
            CPRONUNIVALID=self.cleaned.pron_unicode_is_valid,
            CIPA=self.cleaned.pron_ipastring,
            FIPA=self.filtered.pron_ipastring,
        )



class CleanedPronunciationLexicon(PronunciationLexicon):

    DEFAULT_TEMPLATE = {
        (True, True): u"{CWORDUNI}\t{CPRONUNI}\t{CPRONUNIVALID}",
        (True, False): u"{CWORDUNI}\t{FIPA}",
        (False, True): u"{CWORDUNI}\t{CPRONUNI}",
    }

    PLACEHOLDERS = [
        u"{WORDUNI}",       # (raw) word (Unicode)
        u"{PRONUNI}",       # (raw) pronunciation Unicode string (Unicode)
        u"{PRONUNIVALID}",  # (raw) IPA string is IPA valid (bool)
        u"{IPA}",           # full repr of (raw) IPA string (Unicode)
        u"{CWORDUNI}",      # cleaned+normalized word (Unicode)
        u"{CPRONUNI}",      # cleaned+normalized pronunciation Unicode string (Unicode)
        u"{CPRONUNIVALID}", # cleaned+normalized IPA string is IPA valid (bool)
        u"{CIPA}",          # full repr of cleaned+normalized IPA string (Unicode)
        u"{FIPA}",          # full repr of cleaned+normalized+filtered IPA string (Unicode)
    ]

    ENTRY_TYPE = CleanedPronunciationLexiconEntry

    def apply_cleaner(self, word_cleaner=None, pron_cleaner=None):
        for e in self.entries:
            e.apply_cleaner(word_cleaner=word_cleaner, pron_cleaner=pron_cleaner)

    def pretty_print_stats(self):
        total = len(self.entries)
        raw_valid = len([e for e in self.entries if e.raw.pron_unicode_is_valid])
        raw_valid_perc = 100 * raw_valid / total
        valid = len([e for e in self.entries if e.valid])
        valid_perc = 100 * valid / total
        acc = []
        acc.append(u"Words")
        acc.append(u"  Total:           %d" % total)
        acc.append(u"  Raw Valid:       %d (%0.3f%%)" % (raw_valid, raw_valid_perc))
        acc.append(u"  Raw Invalid:     %d (%0.3f%%)" % (total - raw_valid, 100.0 - raw_valid_perc))
        acc.append(u"  Cleaned Valid:   %d (%0.3f%%)" % (valid, valid_perc))
        acc.append(u"  Cleaned Invalid: %d (%0.3f%%)" % (total - valid, 100.0 - valid_perc))
        return u"\n".join(acc)



