#!/usr/bin/env python
# coding=utf-8

"""
Extract the IPA string from a <page> of the English Wiktionary. 
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

    ==English==
    ...
    ===Pronunciation===
    * {{IPA|/fɹiː/|lang=en}}
    * {{audio|en-us-free.ogg|Audio (US)|lang=en}}
    * {{audio|En-uk-free.ogg|Audio (UK)|lang=en}}
    * {{rhymes|iː|lang=en}}
    ...

    Notes:

    ===Pronunciation===
    * {{a|Canada}} {{IPA|/ənˌsəɪ.kləˈpi.diə/|lang=en}}
    * {{a|UK|US}} {{IPA|/ɪnˌsaɪ.kləˈpi(ː).diə/|lang=en}}
    * {{audio|en-us-encyclopedia.ogg|Audio (US)|lang=en}}
    * {{rhymes|iːdiə|lang=en}}
    * {{hyphenation|en|cy|clo|pe|dia|lang=en}}

    ===Pronunciation===
    * {{a|RP}} {{IPA|/pɔːtˈmæn.təʊ/|lang=en}}
    * {{a|US}} {{enPR|pôrtmă'ntō}}, {{IPA|/pɔɹtˈmæntoʊ/|lang=en}}; {{enPR|pô'rtmăntōʹ}}, {{IPA|/ˌpɔɹtmænˈtoʊ/|lang=en}}
    * {{audio|en-us-portmanteau-1.ogg|Audio 1 (US)|lang=en}}
    * {{audio|en-us-portmanteau-2.ogg|Audio 2 (US)|lang=en}}
    """

    LANGUAGE = "en"
    MW_TYPE = "wiktionary"

    LB_DELIMITER_OPEN = "^=="
    LB_PREFIX = ""
    LB_SUFFIX = ""
    LB_DELIMITER_CLOSE = "==$"
    LB_TARGET = "English"
    
    PB_REGEX = "===Pronunciation==="

    REGEX_1 = re.compile(r"{{IPA\|([^}]*)}}")
    def clean_regex(match):
        parts = match.strip().split(u"|")
        acc = []
        has_lang = False
        for p in parts:
            if (u"lang=en" in p) or (p == u"en"):
                has_lang = True
            if not ((u"lang=" in p) or (p == u"en")):
                acc.append(p)
        if (has_lang) and (len(acc) == 1):
            return acc[0].strip()
        return None
    IPA_REGEXES = [(REGEX_1, clean_regex)]

    IPA_DELIMITERS_OPEN = ["\/"]
    IPA_DELIMITERS_CLOSE = ["\/"]



