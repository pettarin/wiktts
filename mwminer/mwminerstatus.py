#!/usr/bin/env python
# coding=utf-8

"""
Status of the IPA miner, accumulating statistics about the extraction of IPA strings.
"""

from __future__ import absolute_import
from __future__ import division 
from __future__ import print_function

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class MWMinerStatus(object):

    def __init__(self):
        self.mwdata = []
        self.pages_total = 0
        self.pages_with_ipa = 0

    def update(self, chunk_info):
        self.mwdata.extend(chunk_info.mwdata)
        self.pages_total += chunk_info.pages_total
        self.pages_with_ipa += chunk_info.pages_with_ipa

    @property
    def percentage(self):
        p = 0.0
        if self.pages_total > 0:
            p = self.pages_with_ipa / self.pages_total * 100
        return "%.02f%s" % (p, "%")



