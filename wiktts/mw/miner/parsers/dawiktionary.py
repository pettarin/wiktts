#!/usr/bin/env python
# coding=utf-8

"""
Extract the IPA string from a <page> of the Danish Wiktionary. 
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

    {{=da=}}
    ...
    {{-pronun-}}
    *{{IPA|[ˈhunˀ]}}, i sammensætninger {{IPA|[ˈhunə-]}}
    ...
    
    Notes:
    
    *{{IPA|[ˈhunˀ]}}, i sammensætninger {{IPA|[ˈhunə-]}}
    *{{IPA|/miːˀnʹ/|lang=da}}
    *{{IPA|/ˈdænˌmaːɡ/|lang=da}}
    """

    LANGUAGE = "da"
    MW_TYPE = "wiktionary"

    LB_DELIMITER_OPEN = "^{{"
    LB_PREFIX = "="
    LB_SUFFIX = "="
    LB_DELIMITER_CLOSE = "}}$"
    LB_TARGET = "da"

    PB_REGEX = "{{-pronun-}}"

    REGEX_1 = re.compile(r"{{IPA\|([^\|}]*)(\|[^\|}]*)*}}")
    IPA_REGEXES = [(REGEX_1, None)]

    IPA_DELIMITERS_OPEN = ["\/", "\["]
    IPA_DELIMITERS_CLOSE = ["\/", "\]"]



