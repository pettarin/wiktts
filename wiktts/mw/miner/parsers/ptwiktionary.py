#!/usr/bin/env python
# coding=utf-8

"""
Extract the IPA string from a <page> of the Portuguese Wiktionary. 
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
    
    ={{-pt-}}=
    ...
    =={{pronúncia|pt}}==
    ===Brasil===
    * [[SAMPA]]: /e.&quot;sEx.tu/
    * [[AFI]]: /esˈertu/

    ===Portugal===
    * [[AFI]]: {{AFI|/ejʃˈseɾtu/}}, {{AFI|/ejˈʃeɾtu/}}

    Notes:
    
    ==Pronúncia==
    ===Brasil===
    ====Paulistano====
    * IPA: /paw.lis.'tã.nu/
    * SAMPA: /paw.lis.&quot;t6.nu/

    =={{pronúncia|pt}}==
    ===Brasil===
    ====Paulistana e Caipira====
    * AFI: /flu.mi.ˈnẽj.si/
    * SAMPA: /flu.mi.&quot;ne~.si/

    == Pronúncia ==
    '''Brasileira: Paulistana'''
    * AFI: /peɾ.nã.bu.ˈkã.nu/
    * SAMPA: /pex.n6~.bu.k6.nu/

    '''Brasileira: Caipira'''
    * AFI: /peɹ.nã.bu.ˈkã.nu/

    """

    LANGUAGE = "pt"
    MW_TYPE = "wiktionary"

    LB_DELIMITER_OPEN = "^="
    LB_PREFIX = "{{-"
    LB_SUFFIX = "-}}"
    LB_DELIMITER_CLOSE = "=$"
    LB_TARGET = "pt"

    PB_REGEX = u"^==[^pP]*[pP]ronúncia[^=]*==$"  # pronúncia

    REGEX_1 = re.compile(r"{{AFI\|([^\|}]*)(\|[^\|}]*)*}}")
    REGEX_2 = re.compile(r"[\[]*AFI[\]]*: (\/[^\/]*\/)")
    IPA_REGEXES = [(REGEX_1, None), (REGEX_2, None)]

    IPA_DELIMITERS_OPEN = ["\/"]
    IPA_DELIMITERS_CLOSE = ["\/"]



