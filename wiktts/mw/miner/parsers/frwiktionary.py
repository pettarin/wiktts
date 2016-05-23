#!/usr/bin/env python
# coding=utf-8

"""
Extract the IPA string from a <page> of the French Wiktionary. 
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

    == {{langue|fr}} ==
    ...

    === {{S|prononciation}} ===
    * {{pron|slɔ.vak|fr}}

    ...

    Notes:

    * {{écouter|lang=fr|France|slɔ.vɛn(ə)|audio=Fr-slovène.ogg}} => many pages have, instead of {{pron|...}}
    * {{pron|slɔ.vak|fr}} => multiple arguments
    * {{écouter|France (Paris)|ɛ̃ ʒɛn|audio=Fr-gène.ogg|titre=un gène|lang=fr}} => idem
    * {{écouter|Canada {{soutenu|nocat=1}}|ʒɛ̃ːn|lang=fr}} => idem
    * {{écouter|Canada {{informel|nocat=1}}|ʒaɛ̯n|lang=fr}} => idem
    * {{écouter|France|ki.lɔ.mɛtʁ̥], [ki.lo.mɛtʁ̥|lang=fr}} => idem
    """

    LANGUAGE = "fr"
    MW_TYPE = "wiktionary"

    LB_DELIMITER_OPEN = "=="
    LB_PREFIX = "{{langue\|"
    LB_SUFFIX = "}}"
    LB_DELIMITER_CLOSE = "=="
    LB_TARGET = "fr"
    
    PB_REGEX = "=== {{S\|prononciation}} ==="

    REGEX_1 = re.compile(r"{{pron\|([^}]*)}}")
    REGEX_2 = re.compile(r"{{écouter\|([^}]*)}}")
    def clean_regex(match):
        parts = match.strip().split(u"|")
        acc = []
        has_lang = False
        for p in parts:
            if (u"lang=fr" in p) or (u"France" in p) or (p == u"fr"):
                has_lang = True
            if not ((u"lang=" in p) or (u"France" in p) or (u"audio=" in p) or (u"titre=" in p) or (p == u"fr")):
                acc.append(p)
        if (has_lang) and (len(acc) == 1) and (not u"-" in acc[0]) and (not u", " in acc[0]):
            return acc[0].strip()
        return None
    IPA_REGEXES = [(REGEX_1, clean_regex), (REGEX_2, clean_regex)]



