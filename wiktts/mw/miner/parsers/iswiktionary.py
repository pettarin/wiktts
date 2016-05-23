#!/usr/bin/env python
# coding=utf-8

"""
Extract the IPA string from a <page> of the Icelandic Wiktionary. 
"""

from __future__ import absolute_import
from __future__ import print_function
import re

from baseparser import BaseParser

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

__version__ = "0.0.1"
__status__ = "Development"

class Parser(BaseParser):
    """
    Example:

    {{-is-}}
    ...
    {{-framburður-}}
    :{{IPA-is|ipa|tʰ|a|ʰ|k|ː}}
    ...
    
    Notes:
    :{{IPA|[hj̊ar̥.ta], [çar̥.d̥a]}}
    :{{IPA|eintala: [muːs], fleirtala: [miːs]}}

    """

    LANGUAGE = "is"
    MW_TYPE = "wiktionary"

    LB_DELIMITER_OPEN = "^{{"
    LB_PREFIX = "-"
    LB_SUFFIX = "-"
    LB_DELIMITER_CLOSE = "}}$"
    LB_TARGET = "is"
    LB_TARGET_MAX_LENGTH_STOP = 2

    PB_REGEX = u"{{-framburður-}}" 

    REGEX_1 = re.compile(r"{{IPA[^\|]*\|([^}]*)}}")
    def clean_regex(match):
        parts = match.strip().split(u"|")
        ipa_seen = False
        acc = []
        for p in parts:
            if not ipa_seen:
                if p == "ipa":
                    ipa_seen = True
            else:
                acc.append(p)
        if len(acc) > 0:
            return u"".join(acc)
        return None
    REGEX_2 = re.compile(r"{{IPA\|([^\|}]*)(\|[^\|}]*)*}}")
    IPA_REGEXES = [(REGEX_1, clean_regex), (REGEX_2, None)]

    IPA_DELIMITERS_OPEN = ["\["]
    IPA_DELIMITERS_CLOSE = ["\]"]



