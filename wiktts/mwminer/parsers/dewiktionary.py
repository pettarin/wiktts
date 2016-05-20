#!/usr/bin/env python
# coding=utf-8

"""
Extract the IPA string from a <page> of the German Wiktionary. 
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
    
    == Vorteil ({{Sprache|Deutsch}}) ==
    ...

    {{Aussprache}}
    :{{IPA}} {{Lautschrift|ˈfɔʁˌtaɪ̯l}}, auch: {{Lautschrift|ˈfoːɐ̯ˌtaɪ̯l}}
    :{{Hörbeispiele}} {{Audio|}}

    ...

    Notes:

    :{{IPA}} {{Lautschrift|eklaˈtant}}, {{Komp.}} {{Lautschrift|eklaˈtantɐ}}, {{Sup.}} {{Lautschrift|eklaˈtantəstn̩}} => multiple pronunciations
    :{{IPA}} {{Lautschrift|rɔt}}, {{Lautschrift|ˈrɔtər}}, {{Lautschrift|rɔtst}}
    :{{IPA}} {{Lautschrift|…}}, {{Komp.}} {{Lautschrift|…}}, {{Sup.}} {{Lautschrift|…}} => many pages have the tag, but not the actual IPA string
    """
    
    LANGUAGE = "de"
    MW_TYPE = "wiktionary"

    LB_DELIMITER_OPEN = ""
    LB_PREFIX = "{{Sprache\|"
    LB_SUFFIX = "}}"
    LB_DELIMITER_CLOSE = ""
    LB_TARGET = "Deutsch"

    PB_REGEX = "{{Aussprache}}"

    REGEX_1 = re.compile(r":{{IPA}} {{Lautschrift\|([^\|}]*)(\|[^\|}]*)*}}")
    IPA_REGEXES = [(REGEX_1, None)]
    
    IPA_NONE = [u"…"]



