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

from wiktts.ipacleaner.unicleaner import UniCleaner

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

DEFAULT_FORMAT_BOTH = u"{WORD}\t{CIPA}\t{CVALID}"
DEFAULT_FORMAT_VALID = u"{WORD}\t{CIPA}"
DEFAULT_FORMAT_INVALID = u"{WORD}\t{RIPA}"

PLACEHOLDERS = [
    "{RVALID}",     # raw IPA string is IPA valid (bool)
    "{CVALID}",     # cleaned IPA string is IPA valid (bool)
    "{WORD}",       # word (Unicode)
    "{RIPA}",       # raw IPA string (Unicode)
    "{RCV}",        # cns_vwl repr of raw IPA string (Unicode)
    "{RCVS}",       # cns_vwl_str repr of raw IPA string (Unicode)
    "{RCVSL}",      # cns_vwl_str_len repr of raw IPA string (Unicode)
    "{RCVSLW}",     # cns_vwl_str_len_wb repr of raw IPA string (Unicode)
    "{RCVSLWS}",    # cns_vwl_str_len_wb_sb repr of raw IPA string (Unicode)
    "{CIPA}",       # full repr of cleaned+normalized IPA string (Unicode)
    "{CCV}",        # cns_vwl repr of cleaned+normalized IPA string (Unicode)
    "{CCVS}",       # cns_vwl_str repr of cleaned+normalized IPA string (Unicode)
    "{CCVSL}",      # cns_vwl_str_len repr of cleaned+normalized IPA string (Unicode)
    "{CCVSLW}",     # cns_vwl_str_len_wb repr of cleaned+normalized IPA string (Unicode)
    "{CCVSLWS}",    # cns_vwl_str_len_wb_sb repr of cleaned+normalized IPA string (Unicode)
]

class LexiconEntry(object):
    """
    TBW
    """

    def __init__(self, word, cleaned_ipa_unicode, raw_ipa_unicode=None):
        self.word = word
        self.cleaned_ipa_unicode = cleaned_ipa_unicode
        self.cleaned_ipastring = None
        self.raw_ipa_unicode = raw_ipa_unicode
        self.raw_ipastring = None
        self.__cleaned_is_valid = False
        self.__cleaned_valid_chars = []
        self.__cleaned_invalid_chars = []
        self.__raw_is_valid = False
        self._parse()

    def _parse(self):
        self.__cleaned_is_valid = is_valid_ipa(self.cleaned_ipa_unicode)
        self.__raw_is_valid = False
        self.__cleaned_valid_chars, self.__cleaned_invalid_chars = remove_invalid_ipa_characters(
            unicode_string=self.cleaned_ipa_unicode,
            return_invalid=True,
            single_char_parsing=False
        )
        self.cleaned_ipastring = IPAString(
            unicode_string=self.cleaned_ipa_unicode,
            ignore=True,
            single_char_parsing=False
        )
        if self.raw_ipa_unicode is not None:
            self.__raw_is_valid = is_valid_ipa(self.raw_ipa_unicode)
            self.raw_ipastring = IPAString(
                unicode_string=self.raw_ipa_unicode,
                ignore=True,
                single_char_parsing=False
            )

    @property
    def raw_is_valid(self):
        return self.__raw_is_valid

    @property
    def cleaned_is_valid(self):
        return self.__cleaned_is_valid

    @property
    def cleaned_invalid_chars(self):
        return self.__invalid_chars

    @property
    def cleaned_valid_chars(self):
        return self.__valid_chars

    @property
    def canonical_unicode(self):
        return str(self.cleaned_ipastring)



class Lexicon(object):
    """
    TBW
    """

    def __init__(self, clean=False):
        self.entries = []
        self.clean = clean

    def __len__(self):
        return len(self.entries)

    @property
    def raw_valid(self):
        return [e for e in self.entries if e.raw_is_valid]

    @property
    def cleaned_valid(self):
        return [e for e in self.entries if e.cleaned_is_valid]

    def __iter__(self):
        for e in self.entries:
            yield e

    def read_file(self, lexicon_file_path, comment=u"#", delimiter=u"\t", word_index=0, ipa_index=1):
        if (lexicon_file_path is None) or (not os.path.isfile(lexicon_file_path)):
            raise ValueError("The lexicon file path must exist. (Got '%s')" % lexicon_file_path)
        cleaner = UniCleaner()
        comment = to_unicode_string(comment)
        delimiter = to_unicode_string(delimiter)
        u_word = []
        u_raw_ipa = []
        with io.open(lexicon_file_path, "r", encoding="utf-8") as lexicon_file:
            for line in lexicon_file:
                line = line.strip()
                if not line.startswith(comment):
                    acc = line.split(delimiter)
                    u_word.append(acc[word_index])
                    u_raw_ipa.append(acc[ipa_index])
        if self.clean:
            su_cleaned = u_raw_ipa
            su_raw = [None for c in u_raw_ipa]
        else:
            su_raw = u_raw_ipa
            su_cleaned = (cleaner.clean(u"\n".join(u_raw_ipa))).split(u"\n")
        for (w, c, r) in zip(u_word, su_cleaned, su_raw):
            self.entries.append(LexiconEntry(
                word=w,
                cleaned_ipa_unicode=c,
                raw_ipa_unicode=r
            ))

    def phones(self, filter_phones):
        if filter_phones is None:
            filter_phones = DEFAULT_FORMAT_VALID
        s = set()
        for e in self.entries:
            c = e.cleaned_ipastring
            if "{CIPA}" in filter_phones:
                #c = c
                pass
            if "{CCVSLWS}" in filter_phones:
                c = c.cns_vwl_str_len_wb_sb
            elif "{CCVSLW}" in filter_phones:
                c = c.cns_vwl_str_len_wb
            elif "{CCVSL}" in filter_phones:
                c = c.cns_vwl_str_len
            elif "{CCVS}" in filter_phones:
                c = c.cns_vwl_str
            elif "{CCV}" in filter_phones:
                c = c.cns_vwl
            s |= set(c.ipa_chars)
        return s

    def format_phones(self, filter_phones):
        acc = []
        for p in self.phones(filter_phones=filter_phones):
            u = p.unicode_repr
            acc.append(u"'%s'\t%s (%s)" % (u, p.name, unicode_to_hex(u)))
        return sorted(acc)

    def format_lexicon(self, template=None, include_valid=True, include_invalid=False, comment_invalid=False, comment=u"#"):
        # select template
        template = to_unicode_string(template)
        if include_valid and include_invalid:
            template = template or DEFAULT_FORMAT_BOTH
            filtered_data = self.entries
        elif include_valid:
            template = template or DEFAULT_FORMAT_VALID 
            filtered_data = [d for d in self.entries if d.cleaned_is_valid]
        elif include_invalid:
            template = template or DEFAULT_FORMAT_INVALID
            filtered_data = [d for d in self.entries if not d.cleaned_is_valid]
        else:
            template = template or DEFAULT_FORMAT_BOTH
            filtered_data = []

        if comment_invalid:
            template = u"{COMMENT}" + template
            comment += u" "

        # format data
        return [template.format(
            COMMENT=(u"" if d.cleaned_is_valid else comment),
            RVALID=d.raw_is_valid,
            CVALID=d.cleaned_is_valid,
            WORD=d.word,
            RIPA=d.raw_ipa_unicode,
            RCV=d.raw_ipastring.cns_vwl,
            RCVS=d.raw_ipastring.cns_vwl_str,
            RCVSL=d.raw_ipastring.cns_vwl_str_len,
            RCVSLW=d.raw_ipastring.cns_vwl_str_len_wb,
            RCVSLWS=d.raw_ipastring.cns_vwl_str_len_wb_sb,
            CIPA=d.cleaned_ipa_unicode,
            CCV=d.cleaned_ipastring.cns_vwl,
            CCVS=d.cleaned_ipastring.cns_vwl_str,
            CCVSL=d.cleaned_ipastring.cns_vwl_str_len,
            CCVSLW=d.cleaned_ipastring.cns_vwl_str_len_wb,
            CCVSLWS=d.cleaned_ipastring.cns_vwl_str_len_wb_sb,
        ) for d in filtered_data]



