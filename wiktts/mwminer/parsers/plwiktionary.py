#!/usr/bin/env python
# coding=utf-8

"""
Extract the IPA string from a <page> of the Polish Wiktionary. 
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
    == czytać ({{język polski}}) ==
    ...
    {{wymowa}} {{IPA3|ˈʧ̑ɨtaʨ̑}}, {{AS3|č'''y'''tać}} {{audio|Pl-czytać.ogg}}
    ...

    Notes:
    {{wymowa}} {{IPA3|pʃɛˈʧ̑ɨtaʨ̑}}, {{AS3|pšeč'''y'''tać}}, {{objaśnienie wymowy|BDŹW}} {{audio|Pl-przeczytać.ogg}}
    {{wymowa}} {{lp}} {{audio|Pl-dom.ogg}}, {{IPA3|dɔ̃m}}, {{AS3|dõm}}, {{objaśnienie wymowy|NAZAL}}; {{lm}} {{IPA2|ˈdɔmɨ}}
    """
    
    LANGUAGE = "pl"
    MW_TYPE = "wiktionary"

    LB_DELIMITER_OPEN = ""
    LB_PREFIX = u"{{język "
    LB_SUFFIX = "}}"
    LB_DELIMITER_CLOSE = ""
    LB_TARGET = "polski"

    PB_REGEX = "{{wymowa}}"

    REGEX_1 = re.compile(r"{{IPA3\|([^\|}]*)(\|[^\|}]*)*}}")
    IPA_REGEXES = [(REGEX_1, None)]
    


