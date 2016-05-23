#!/usr/bin/env python
# coding=utf-8

"""
Extract the IPA string from a <page> of the Svedish Wiktionary. 
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

    ==Svenska==
    ...
    *{{uttal|ipa=hɵnd}}
    ...

    Notes:
    
    *{{uttal|enkel=|ipa=jʉːl}}
    *{{uttal|ipa=ɛˈleːvən|språk=svenska}}
    """

    LANGUAGE = "sv"
    MW_TYPE = "wiktionary"

    LB_DELIMITER_OPEN = "^=="
    LB_PREFIX = ""
    LB_SUFFIX = ""
    LB_DELIMITER_CLOSE = "==$"
    LB_TARGET = "Svenska"

    REGEX_1 = re.compile(r"{{uttal\|([^}]*)}}")
    def clean_regex(match):
        parts = match.strip().split(u"|")
        for p in parts:
            if (u"språk" in p) and (p != u"språk=svenska"):
                return None
            if p.startswith("ipa="):
                return p[4:].strip()
        return None
    IPA_REGEXES = [(REGEX_1, clean_regex)]



