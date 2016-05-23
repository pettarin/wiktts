#!/usr/bin/env python
# coding=utf-8

"""
Load an IPA parser dynamically (from file name or file path),
and use it to extract IPA strings from a file, a list of Page objects, or a string.
"""

from __future__ import absolute_import
from __future__ import division 
from __future__ import print_function
import imp
import os

from wiktts.mw.data import Data
from wiktts.mw.data import ExtractionInfo
from wiktts.mw.parser import Parser

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class IPAExtractor(object):
    
    PARSERS_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(__file__)), "parsers")

    def __init__(self, ipa_parser_name):
        try:
            if os.path.isfile(ipa_parser_name):
                ipa_parser_code = imp.load_source("", ipa_parser_name)
            else:
                ipa_parser_full_path = ipa_parser_name
                if not ipa_parser_full_path.endswith(".py"):
                    ipa_parser_full_path += ".py"
                base_parser = imp.load_source("baseparser", os.path.join(self.PARSERS_DIRECTORY, "baseparser.py"))
                ipa_parser_code = imp.load_source("", os.path.join(self.PARSERS_DIRECTORY, ipa_parser_full_path))
        except:
            raise ValueError("Unable to load parser. (Got '%s')" % ipa_parser_name)
        self.ipa_parser = ipa_parser_code.Parser()

    def extract_from_file(self, dump_file_path):
        return self.extract_from_pages(Parser(full_parsing=False).parse_file(dump_file_path).pages)

    def extract_from_pages(self, pages):
        mwdata = []
        pages_with_ipa = 0
        for p in pages:
            ipa = self.ipa_parser.extract_ipa_string(p.revision_text)
            if (len(p.title) > 0) and (ipa is not None) and (len(ipa) > 0):
                mwdata.append(Data(True, p.id, p.title, ipa))
                pages_with_ipa += 1
            else:
                mwdata.append(Data(False, p.id, p.title, None))
        return ExtractionInfo(mwdata=mwdata, pages_total=len(pages), pages_with_ipa=pages_with_ipa)

    def extract_from_string(self, string):
        return self.ipa_parser.extract_ipa_string(string)



