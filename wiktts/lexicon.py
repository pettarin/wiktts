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

DEFAULT_FORMAT_BOTH = u"{CWORD}\t{CIPA}\t{CVALID}"
DEFAULT_FORMAT_VALID = u"{CWORD}\t{CIPA}"
DEFAULT_FORMAT_INVALID = u"{RWORD}\t{RIPA}"

PLACEHOLDERS = [
    "{RWORD}",      # raw word (Unicode)
    "{CWORD}",      # cleaned word (Unicode)
    "{RVALID}",     # raw IPA string is IPA valid (bool)
    "{CVALID}",     # cleaned IPA string is IPA valid (bool)
    "{RUNI}",       # raw Unicode string (Unicode)
    "{RIPA}",       # full repr of raw IPA string (Unicode)
    "{RCV}",        # cns_vwl repr of raw IPA string (Unicode)
    "{RCVP}",       # cns_vwl_pstr repr of raw IPA string (Unicode)
    "{RCVS}",       # cns_vwl_str repr of raw IPA string (Unicode)
    "{RCVPL}",      # cns_vwl_pstr_long repr of raw IPA string (Unicode)
    "{RCVSL}",      # cns_vwl_str_len repr of raw IPA string (Unicode)
    "{RCVSLW}",     # cns_vwl_str_len_wb repr of raw IPA string (Unicode)
    "{RCVSLWS}",    # cns_vwl_str_len_wb_sb repr of raw IPA string (Unicode)
    "{CIPA}",       # cleaned Unicode string (Unicode)
    "{CIPA}",       # full repr of cleaned+normalized IPA string (Unicode)
    "{CCV}",        # cns_vwl repr of cleaned+normalized IPA string (Unicode)
    "{CCVP}",       # cns_vwl_pstr repr of cleaned+normalized IPA string (Unicode)
    "{CCVS}",       # cns_vwl_str repr of cleaned+normalized IPA string (Unicode)
    "{CCVPL}",      # cns_vwl_pstr_long repr of cleaned+normalized IPA string (Unicode)
    "{CCVSL}",      # cns_vwl_str_len repr of cleaned+normalized IPA string (Unicode)
    "{CCVSLW}",     # cns_vwl_str_len_wb repr of cleaned+normalized IPA string (Unicode)
    "{CCVSLWS}",    # cns_vwl_str_len_wb_sb repr of cleaned+normalized IPA string (Unicode)
]

class LexiconEntry(object):
    """
    TBW
    """

    def __init__(self, clean, raw_word_unicode, cleaned_word_unicode, raw_ipa_unicode, cleaned_ipa_unicode):
        # store
        self.clean = clean
        self.raw_word_unicode = raw_word_unicode
        self.cleaned_word_unicode = cleaned_word_unicode
        self.raw_ipa_unicode = raw_ipa_unicode
        self.cleaned_ipa_unicode = cleaned_ipa_unicode
        # derive 
        self.raw_ipastring = None
        self.cleaned_ipastring = None
        self.__raw_is_valid = False
        self.__cleaned_is_valid = False
        self.__cleaned_valid_chars = []
        self.__cleaned_invalid_chars = []
        self._parse()

    def _parse(self):
        # cleaned IPA
        self.__cleaned_is_valid = is_valid_ipa(self.cleaned_ipa_unicode)
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
        # raw IPA
        self.__raw_is_valid = False
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

    def __init__(self, clean=False, word_cleaner=None, ipa_cleaner=None):
        self.entries = []
        self.clean = clean
        self.word_cleaner = word_cleaner
        self.ipa_cleaner = ipa_cleaner

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
        comment = to_unicode_string(comment)
        delimiter = to_unicode_string(delimiter)
        u_raw_word = []
        u_raw_ipa = []
        with io.open(lexicon_file_path, "r", encoding="utf-8") as lexicon_file:
            for line in lexicon_file:
                line = line.strip()
                if not line.startswith(comment):
                    acc = line.split(delimiter)
                    u_raw_word.append(acc[word_index])
                    u_raw_ipa.append(acc[ipa_index])

        if (not self.clean) and (self.word_cleaner is not None):
            u_clean_word = (self.word_cleaner.clean(u"\n".join(u_raw_word))).split(u"\n")
        else:
            u_clean_word = u_raw_word

        if (not self.clean) and (self.ipa_cleaner is not None):
            u_clean_ipa = (self.ipa_cleaner.clean(u"\n".join(u_raw_ipa))).split(u"\n")
        else:
            u_clean_ipa = u_raw_ipa

        for (rw, cw, ri, ci) in zip(u_raw_word, u_clean_word, u_raw_ipa, u_clean_ipa):
            self.entries.append(LexiconEntry(
                clean=self.clean,
                raw_word_unicode=rw,
                cleaned_word_unicode=cw,
                raw_ipa_unicode=ri,
                cleaned_ipa_unicode=ci
            ))

    def phones(self, filter_phones):
        if filter_phones is None:
            filter_phones = DEFAULT_FORMAT_VALID
        if "{CIPA}" in filter_phones:
            ent = [e.cleaned_ipastring for e in self.entries]
        elif "{CCVSLWS}" in filter_phones:
            ent = [e.cleaned_ipastring.cns_vwl_str_len_wb_sb for e in self.entries]
        elif "{CCVSLW}" in filter_phones:
            ent = [e.cleaned_ipastring.cns_vwl_str_len_wb for e in self.entries]
        elif "{CCVSL}" in filter_phones:
            ent = [e.cleaned_ipastring.cns_vwl_str_len for e in self.entries]
        elif "{CCVPL}" in filter_phones:
            ent = [e.cleaned_ipastring.cns_vwl_pstr_long for e in self.entries]
        elif "{CCVS}" in filter_phones:
            ent = [e.cleaned_ipastring.cns_vwl_str for e in self.entries]
        elif "{CCVP}" in filter_phones:
            ent = [e.cleaned_ipastring.cns_vwl_pstr for e in self.entries]
        elif "{CCV}" in filter_phones:
            ent = [e.cleaned_ipastring.cns_vwl for e in self.entries]
        else:
            ent = [e.cleaned_ipastring for e in self.entries]
        s = set()
        for e in ent:
            s |= set(e.ipa_chars)
        return s

    def format_phones(self, filter_phones):
        acc = []
        for p in self.phones(filter_phones=filter_phones):
            u = p.unicode_repr
            acc.append(u"'%s'\t%s (%s)" % (u, p.name, unicode_to_hex(u)))
        return sorted(acc)

    def format_letters(self):
        letters = set()
        for e in self.entries:
            letters |= set(e.cleaned_word_unicode)
        acc = []
        for l in letters:
            acc.append(u"'%s'\t%s (%s)" % (l, unicodedata.name(l, u"UNKNOWN"), unicode_to_hex(l)))
        return sorted(acc)

    def format_lexicon(self, template=None, include_valid=True, include_invalid=False, comment_invalid=False, comment=u"#"):
        # working with Unicode
        template = to_unicode_string(template)
        
        # select template
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
        
        # add comment field to template
        if comment_invalid:
            template = u"{COMMENT}" + template
            comment += u" "

        # format data
        return [template.format(
            COMMENT=(u"" if d.cleaned_is_valid else comment),
            RVALID=d.raw_is_valid,
            CVALID=d.cleaned_is_valid,
            RWORD=d.raw_word_unicode,
            CWORD=d.cleaned_word_unicode,
            RUNI=d.raw_ipa_unicode,
            RIPA=d.raw_ipastring,
            RCV=d.raw_ipastring.cns_vwl,
            RCVP=d.raw_ipastring.cns_vwl_pstr,
            RCVS=d.raw_ipastring.cns_vwl_str,
            RCVPL=d.raw_ipastring.cns_vwl_pstr_long,
            RCVSL=d.raw_ipastring.cns_vwl_str_len,
            RCVSLW=d.raw_ipastring.cns_vwl_str_len_wb,
            RCVSLWS=d.raw_ipastring.cns_vwl_str_len_wb_sb,
            CUNI=d.cleaned_ipa_unicode,
            CIPA=d.cleaned_ipastring,
            CCV=d.cleaned_ipastring.cns_vwl,
            CCVP=d.cleaned_ipastring.cns_vwl_pstr,
            CCVS=d.cleaned_ipastring.cns_vwl_str,
            CCVPL=d.cleaned_ipastring.cns_vwl_pstr_long,
            CCVSL=d.cleaned_ipastring.cns_vwl_str_len,
            CCVSLW=d.cleaned_ipastring.cns_vwl_str_len_wb,
            CCVSLWS=d.cleaned_ipastring.cns_vwl_str_len_wb_sb,
        ) for d in filtered_data]



