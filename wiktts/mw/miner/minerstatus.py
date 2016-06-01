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
__email__ = "alberto@albertopettarin.it"

class MinerStatus(object):

    def __init__(self):
        self.mwdata = []
        self.pages_total = 0
        self.pages_with_language_block = 0
        self.pages_with_ipa = 0

    def _percentage(self, value):
        p = 0.0
        if self.pages_total > 0:
            p = value / self.pages_total * 100
        return p

    @property
    def pages_with_language_block_percentage(self):
        return self._percentage(self.pages_with_language_block)

    @property
    def pages_with_ipa_percentage(self):
        return self._percentage(self.pages_with_ipa)

    def update(self, chunk_info):
        self.mwdata.extend(chunk_info.mwdata)
        self.pages_total += chunk_info.pages_total
        self.pages_with_language_block += chunk_info.pages_with_language_block
        self.pages_with_ipa += chunk_info.pages_with_ipa

    def pretty_print(self, single_line=False):
        if single_line:
            ret = u"Pages Total/Language/IPA:   %d / %d / %d   (100%% / %.3f%% / %.3f%%)" % (
                self.pages_total,
                self.pages_with_language_block,
                self.pages_with_ipa,
                self.pages_with_language_block_percentage,
                self.pages_with_ipa_percentage
            )
        else:
            acc = []
            acc.append(u"Pages")
            acc.append(u"  Total:               %d" % self.pages_total)
            acc.append(u"  With Language Block: %d (%.3f%%)" % (self.pages_with_language_block, self.pages_with_language_block_percentage))
            acc.append(u"  With IPA:            %d (%.3f%%)" % (self.pages_with_ipa, self.pages_with_ipa_percentage))
            ret = u"\n".join(acc)
        return ret




