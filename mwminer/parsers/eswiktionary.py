#!/usr/bin/env python
# coding=utf-8

"""
Extract the IPA string from a <page> of the Spanish Wiktionary. 
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

    == {{lengua|es}} ==
    {{pron-graf|fone=o.lanˈdes}}
    ...

    Notes:
    
    {{pron-graf}}
    {{pron-graf|fone=ˈu.ni|p=unir|palt=uní}}
    {{pron-graf|pron=seseo|altpron=No seseante|fone=ko.noˈθeɾ|2pron=seseo|alt2pron=Seseante|2fone=ko.noˈseɾ}}
    {{pron-graf|fone=o.la|h=hola}}
    {{pron-graf|pron=seseo|altpron=No seseante|fone=re.ko.lek.ˈθjon|2pron=seseo|alt2pron=Seseante|2fone=re.ko.lek.ˈsjoŋ}}
    """

    LANGUAGE = "es"
    MW_TYPE = "wiktionary"

    LB_DELIMITER_OPEN = "=="
    LB_PREFIX = "{{lengua\|"
    LB_SUFFIX = "}}"
    LB_DELIMITER_CLOSE = "=="
    LB_TARGET = "es"

    REGEX_1 = re.compile(r"{{pron-graf\|([^}]*)}}")
    def clean_regex(match):
        parts = match.strip().split(u"|")
        acc = []
        has_lang = False
        for p in parts:
            if p.startswith(u"fone="):
                return p[5:].strip()
        return None
    IPA_REGEXES = [(REGEX_1, clean_regex)]

    IPA_DELIMITERS_OPEN = []
    IPA_DELIMITERS_CLOSE = []

    IPA_NONE = []



