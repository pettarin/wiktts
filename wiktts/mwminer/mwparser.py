#!/usr/bin/env python
# coding=utf-8

"""
Parse MediaWiki dump files, exposing user-friendly
functions to access their pages.
"""

from __future__ import absolute_import
from __future__ import print_function
from lxml import etree
import os
import sys

from wiktts.mwminer.mwpage import MWPage

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

NAMESPACES = {"ns": "http://www.mediawiki.org/xml/export-0.10/"}

class MWParser(object):

    def __init__(self, full_parsing=False):
        self.pages = []
        self.full_parsing = full_parsing

    def _check_dump_file_path(self, dump_file_path):
        if dump_file_path == "-":
            return sys.stdin
        elif (dump_file_path is None) or (not os.path.isfile(dump_file_path)):
            raise ValueError("The dump file path must exist. (Got '%s')" % dump_file_path)
        return dump_file_path

    def clear(self):
        self.pages = []

    def parse_file(self, dump_file_path, append=False):
        input_file = self._check_dump_file_path(dump_file_path)
        root = etree.parse(input_file).getroot()
        return self._parse(root=root, append=append)

    def parse_string(self, string, append=False):
        try:
            string = string.encode("utf-8")
        except:
            pass
        root = etree.fromstring(string)
        return self._parse(root=root, append=append)

    def _parse(self, root, append=False):
        if not append:
            self.clear()
        for page in root.xpath("ns:page", namespaces=NAMESPACES):
            self.pages.append(MWPage(page, full_parsing=self.full_parsing))
        return self



