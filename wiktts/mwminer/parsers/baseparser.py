#!/usr/bin/env python
# coding=utf-8

"""
Common functions to parse MediaWiki markup to extract IPA strings. 
"""

from __future__ import absolute_import
from __future__ import print_function
import re

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class BaseParser(object):
    
    # base properties of the parser
    LANGUAGE = "" # 
    MW_TYPE = "" # Wiktionary or Wikipedia 

    # start the language block
    LB_DELIMITER_OPEN = ""
    LB_PREFIX = ""
    LB_SUFFIX = ""
    LB_DELIMITER_CLOSE = ""
    LB_TARGET = ""
    LB_TARGET_MAX_LENGTH_STOP = None

    # start the pronunciation block
    PB_REGEX = None

    # regex to match IPA strings
    IPA_REGEXES = []

    # remove the following IPA string delimiters
    IPA_DELIMITERS_OPEN = []
    IPA_DELIMITERS_CLOSE = []
    
    # output None if the matched IPA string is in the list
    # this is used e.g. in German, where a placeholder character is present
    # but the actual IPA string is not available
    IPA_NONE = []

    def __init__(self):
        # match language block start
        if len(self.LB_SUFFIX) > 0:
            self.lb_regex = re.compile(
                self.LB_DELIMITER_OPEN +
                u"[ ]*" +
                self.LB_PREFIX +
                u"([^" +
                self.LB_SUFFIX[0] +
                u"]*)" +
                self.LB_SUFFIX +
                u"[ ]*" +
                self.LB_DELIMITER_CLOSE,
                flags=re.UNICODE
            )
        else:
            self.lb_regex = re.compile(
                self.LB_DELIMITER_OPEN +
                u"([^" +
                self.LB_DELIMITER_CLOSE[0] +
                u"]*)" +
                self.LB_DELIMITER_CLOSE,
                flags=re.UNICODE
            )

        # match pronunciation block start
        if self.PB_REGEX is not None:
            self.pb_regex = re.compile(self.PB_REGEX, flags=re.UNICODE)
        else:
            self.pb_regex = None

        # match and remove IPA string delimiters
        self.ipa_delimiter_regex = None
        if len(self.IPA_DELIMITERS_OPEN) + len(self.IPA_DELIMITERS_CLOSE) > 0:
            self.ipa_delimiter_regex = re.compile(
                u"[" +
                u"".join(self.IPA_DELIMITERS_OPEN) +
                u"]*" +
                u"(.*)" +
                u"[" +
                u"".join(self.IPA_DELIMITERS_CLOSE) +
                u"]*",
                flags=re.UNICODE
            )

    def extract_ipa_string(self, text):
        """
        Extract the IPA string from the given string,
        representing the wikitext of a <page> (i.e., a word).
        """
        lb_lines = self.find_language_block(text)
        if lb_lines is None:
            return None
        #print("=== LANGUAGE BLOCK ===")
        #for line in lb_lines:
        #    print(line)
        #print("=== LANGUAGE BLOCK ===")
        #print("")

        pb_lines = self.find_pronunciation_block(lb_lines)
        if pb_lines is None:
            return None
        #print("=== PRONUNCIATION BLOCK ===")
        #for line in pb_lines:
        #    print(line)
        #print("=== PRONUNCIATION BLOCK  ===")
        #print("")
        
        ipa = self.find_ipa(pb_lines)
        if ipa is None:
            return None

        ipa = self.keep_first_only(ipa)
        ipa = self.remove_ipa_delimiters(ipa)
        if ipa in self.IPA_NONE:
            return None
        return ipa 

    def remove_ipa_delimiters(self, ipa_candidate):
        """
        Remove the IPA delimiters.
        """
        if self.ipa_delimiter_regex is not None:
            m = re.match(self.ipa_delimiter_regex, ipa_candidate)
            if m is not None:
                return m.group(1).strip()
        return ipa_candidate

    def keep_first_only(self, ipa):
        """
        In case of multiple IPA strings, separated by ", ",
        return only the first one.
        """
        index = min(ipa.find(u", "), len(ipa))
        return ipa[:index]

    def find_ipa(self, lines):
        """
        Return the first matching IPA string.
        """
        for line in lines:
            for regex, func in self.IPA_REGEXES:
                m = re.search(regex, line)
                if m is not None:
                    if func is None:
                        res = m.group(1).strip()
                    else:
                        res = func(m.group(1))
                    if res is not None:
                        return res
        return None

    def find_pronunciation_block(self, lines):
        """
        Find the pronunciation block.
        """
        if self.pb_regex is None:
            return lines
        inside = False
        start = -1
        stop = -1
        for i in range(len(lines)):
            line = lines[i]
            if inside:
                if len(line.strip()) == 0:
                    stop = i
                    break
            else:
                m = re.search(self.pb_regex, line)
                if m is not None:
                    start = i
                    inside = True
        if stop == -1:
            stop = len(lines)
        if start > -1:
            return lines[start:stop]
        return None

    def find_language_block(self, text):
        """
        Find the correct language block.
        """
        inside = False
        start = -1
        stop = -1
        lines = text.split("\n")
        for i in range(len(lines)):
            line = lines[i]
            m = re.search(self.lb_regex, line)
            if m is not None:
                if inside:
                    if (self.LB_TARGET_MAX_LENGTH_STOP is None) or (len(m.group(1)) <= self.LB_TARGET_MAX_LENGTH_STOP):
                        stop = i
                        break
                elif m.group(1) == self.LB_TARGET:
                    start = i
                    inside = True
        if stop == -1:
            stop = len(lines)
        if start > -1:
            return lines[start:stop]
        return None



