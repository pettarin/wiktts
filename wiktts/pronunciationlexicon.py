#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unicodedata

from ipapy.compatibility import to_unicode_string
from ipapy.compatibility import unicode_to_hex

from wiktts.lexicon import Lexicon
from wiktts.lexicon import LexiconEntry
from wiktts.wordpronunciationpair import WordPronunciationPair

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class PronunciationLexiconEntry(LexiconEntry):

    def __init__(self, raw_values, lowercase=False):
        self.raw = None
        self.filtered = None
        super(PronunciationLexiconEntry, self).__init__(raw_values=raw_values, lowercase=lowercase)

    def _set_value(self, raw_values, lowercase):
        if len(raw_values) >= 2:
            word_unicode=raw_values[0]
            pron_unicode=raw_values[1]
            if lowercase:
                word_unicode = word_unicode.lower()
            self.raw = WordPronunciationPair(
                word_unicode=word_unicode,
                pron_unicode=pron_unicode
            )
            self.filtered = self.raw
            self.valid = self.raw.pron_unicode_is_valid
            self.value = self.raw.pron_ipastring

    def _format_template(self, template):
        return template.format(
            WORDUNI=self.raw.word_unicode,
            PRONUNI=self.raw.pron_unicode,
            PRONUNIVALID=self.raw.pron_unicode_is_valid,
            IPA=self.raw.pron_ipastring,
            FIPA=self.filtered.pron_ipastring,
        )

    def format(self, template, comment_string=u""):
        ret = self._format_template(template)
        if self.valid:
            return ret
        return comment_string + ret

    def filter_chars(self, chars):
        self.filtered = WordPronunciationPair(
            word_unicode=self.raw.word_unicode,
            pron_ipastring=self.raw.pron_ipastring.filter_chars(chars=chars)
        )
        self.value = self.filtered.pron_ipastring

    @property
    def letters(self):
        return self.filtered.letters 

    @property
    def phones(self):
        return self.filtered.phones

    @property
    def value_as_sequence(self):
        return self.value.ipa_chars 



class PronunciationLexicon(Lexicon):
    """
    TBW
    """

    DEFAULT_TEMPLATE = {
        (True, True): u"{WORDUNI}\t{PRONUNI}\t{PRONUNIVALID}",
        (True, False): u"{WORDUNI}\t{FIPA}",
        (False, True): u"{WORDUNI}\t{PRONUNI}",
    }

    PLACEHOLDERS = [
        u"{WORDUNI}",      # word (Unicode)
        u"{PRONUNI}",      # pronunciation Unicode string (Unicode)
        u"{PRONUNIVALID}", # pronunciation Unicode string is IPA valid (bool)
        u"{IPA}",          # full repr of IPA string (Unicode)
        u"{FIPA}",         # full repr of filtered IPA string (Unicode)
    ]

    FILTER_IPA_CHARS = [
        u"all",
        u"letters",
        u"cvp",
        u"cvs",
        u"cvpl",
        u"cvsl",
        u"cvslw",
        u"cvslws",
    ]

    ENTRY_TYPE = PronunciationLexiconEntry

    def __init__(self, entries=None, lowercase=False):
        self.include_valid = True
        self.include_invalid = False
        super(PronunciationLexicon, self).__init__(entries=entries, lowercase=lowercase)

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
    def phones(self):
        phones = set()
        for e in self:
            phones |= e.phones
        return phones

    def filter_chars(self, chars):
        if chars == u"all":
            return
        for e in self:
            e.filter_chars(chars=chars)

    def format_letters(self):
        return sorted([(u"%s\t%s\t%s" % (l, unicode_to_hex(l), unicodedata.name(l, u"UNKNOWN"))) for l in self.letters])

    def format_phones(self):
        return sorted([(u"%s\t%s (%s)" % (p.unicode_repr, p.name, unicode_to_hex(p.unicode_repr))) for p in self.phones])

    def format_lexicon(self, template=None, comment_invalid=False, comment=u"#", sort=False):
        template = to_unicode_string(template) or self.DEFAULT_TEMPLATE[(self.include_valid, self.include_invalid)]
        comment_string = comment if comment_invalid else u""
        formatted_data = [e.format(template, comment_string) for e in self]
        if sort:
            return sorted(formatted_data)
        return formatted_data 

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



