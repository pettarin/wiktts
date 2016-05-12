#!/usr/bin/env python
# coding=utf-8

"""
Extract the IPA string from a <page> of the Norwegian Wiktionary. 
"""

from __future__ import absolute_import
from __future__ import print_function
import re

from baseparser import BaseParser

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class Parser(BaseParser):
    """
    Example:

    ==Norsk==
    ...
    ====Uttale====
    *{{IPA|/veps/|språk=no}}
    ...

    Notes:

    {{uttale mangler|språk=no}}
    {{lyd mangler|språk=no}}
    * {{IPA|[ˈkʋel]|språk=no}}
    """

    LANGUAGE = "no"
    MW_TYPE = "wiktionary"

    LB_DELIMITER_OPEN = "^=="
    LB_PREFIX = ""
    LB_SUFFIX = ""
    LB_DELIMITER_CLOSE = "==$"
    LB_TARGET = "Norsk"
   
    PB_REGEX = "====Uttale===="

    REGEX_1 = re.compile(r"{{IPA\|([^}]*)}}")
    def clean_regex(match):
        parts = match.strip().split(u"|")
        acc = []
        has_lang = False
        for p in parts:
            if (u"språk=no" in p) or (p == u"no") or (u"språk=nb" in p) or (p == u"nb"):
                has_lang = True
            if not ((u"språk=" in p) or (p == u"no") or (p == u"nb")):
                acc.append(p)
        if (has_lang) and (len(acc) == 1):
            return acc[0].strip()
        return None
    IPA_REGEXES = [(REGEX_1, clean_regex)]

    IPA_DELIMITERS_OPEN = ["\/", "\["]
    IPA_DELIMITERS_CLOSE = ["\/", "\]"]



