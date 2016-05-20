#!/usr/bin/env python
# coding=utf-8

"""
A MediaWiki ``<page>`` object.
"""

from __future__ import absolute_import
from __future__ import print_function

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

NAMESPACES = {"ns": "http://www.mediawiki.org/xml/export-0.10/"}

class MWPage(object):
    
    def __init__(self, page_obj, full_parsing=False):
        self.id = None
        self.title = None
        self.ns = None
        self.revision_id = None
        self.revision_timestamp = None
        self.revision_text = None
        self._parse(page_obj, full_parsing)

    def _parse(self, p, full_parsing=False):
        self.id = p.xpath("ns:id", namespaces=NAMESPACES)[0].text
        self.title = p.xpath("ns:title", namespaces=NAMESPACES)[0].text or ""
        revision = p.xpath("ns:revision", namespaces=NAMESPACES)[0]
        self.revision_text = revision.xpath("ns:text", namespaces=NAMESPACES)[0].text or ""
        if full_parsing:
            self.ns = p.xpath("ns:ns", namespaces=NAMESPACES)[0].text
            self.revision_id = revision.xpath("ns:id", namespaces=NAMESPACES)[0].text
            self.revision_timestamp = revision.xpath("ns:timestamp", namespaces=NAMESPACES)[0].text



