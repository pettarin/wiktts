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

class MappedPronunciationLexiconEntry(PronunciationLexiconEntry):

    def apply_mapper(self, mapper):
        self.valid = mapper.can_map_ipa_string(self.filtered.pron_ipastring)
        if self.valid:
            self.value = mapper.map_ipa_string(self.filtered.pron_ipastring, ignore=False, return_as_list=True)

    def _format_template(self, template):
        return template.format(
            WORDUNI=self.raw.word_unicode,
            PRONUNI=self.raw.pron_unicode,
            PRONUNIVALID=self.raw.pron_unicode_is_valid,
            IPA=self.raw.pron_ipastring,
            FIPA=self.filtered.pron_ipastring,
            FMAPPABLE=self.valid,
            MVALUE=self.value
        )

    @property
    def symbols(self):
        if self.valid:
            return set(self.value)
        return set()



class MappedPronunciationLexicon(PronunciationLexicon):

    DEFAULT_TEMPLATE = {
        (True, True): u"{WORDUNI}\t{PRONUNI}\t{FMAPPABLE}",
        (True, False): u"{MWORDUNI}\t{MVALUE}",
        (False, True): u"{WORDUNI}\t{PRONUNI}",
    }

    PLACEHOLDERS = [
        u"{WORDUNI}",      # word (Unicode)
        u"{PRONUNI}",      # pronunciation Unicode string (Unicode)
        u"{PRONUNIVALID}", # pronunciation Unicode string is IPA valid (bool)
        u"{IPA}",          # full repr of IPA string (Unicode)
        u"{FIPA}",         # full repr of filtered IPA string (Unicode)
        u"{FMAPPABLE}",    # filtered IPA string is mappable
        u"{MVALUE}",       # mapped value
    ]

    ENTRY_TYPE = MappedPronunciationLexiconEntry

    @property
    def symbols(self):
        symbols = set()
        for e in self:
            symbols |= e.symbols
        return symbols

    def apply_mapper(self, mapper):
        for e in self:
            e.apply_mapper(mapper=mapper)

    def pretty_print_stats(self):
        total = len(self)
        raw_valid = len([e for e in self if e.raw.pron_unicode_is_valid])
        raw_valid_perc = 100 * raw_valid / total
        valid = len([e for e in self if e.valid])
        valid_perc = 100 * valid / total
        acc = []
        acc.append(u"Words")
        acc.append(u"  Total:                %d" % total)
        acc.append(u"  Raw/Filtered Valid:   %d (%0.3f%%)" % (raw_valid, raw_valid_perc))
        acc.append(u"  Raw/Filtered Invalid: %d (%0.3f%%)" % (total - raw_valid, 100.0 - raw_valid_perc))
        acc.append(u"  Mapped Valid:         %d (%0.3f%%)" % (valid, valid_perc))
        acc.append(u"  Mapped Invalid:       %d (%0.3f%%)" % (total - valid, 100.0 - valid_perc))
        return u"\n".join(acc)



