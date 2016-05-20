#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class ICCleaner(object):

    def clean(self, s):
        # lowercase
        s = s.lower()
       
        # long
        s = s.replace(u"\u003A", u"\u02D0") # COLON
        
        # primary-stress
        s = s.replace(u"\u0022", u"\u02C8") # QUOTATION MARK
        s = s.replace(u"\u0027", u"\u02C8") # APOSTROPHE
        s = s.replace(u"\u0060", u"\u02C8") # GRAVE ACCENT
        s = s.replace(u"\u00B4", u"\u02C8") # ACUTE ACCENT
        s = s.replace(u"\u02B9", u"\u02C8") # MODIFIER LETTER PRIME
        s = s.replace(u"\u2018", u"\u02C8") # LEFT SINGLE QUOTATION MARK
        s = s.replace(u"\u2019", u"\u02C8") # RIGHT SINGLE QUOTATION MARK
        s = s.replace(u"\u2032", u"\u02C8") # PRIME
       
        # secondary-stress
        s = s.replace(u"\u002C", u"\u02CC") # COMMA
        s = s.replace(u"\u0375", u"\u02CC") # GREEK LOWER NUMERAL SIGN
        s = s.replace(u"\u201A", u"\u02CC") # SINGLE LOW-9 QUOTATION MARK

        # syllable-break ('.' FULL STOP)
        s = s.replace(u"\u00B7", u"\u002E") # MIDDLE DOT
        s = s.replace(u"\u2027", u"\u002E") # HYPHENATION POINT

        # word-break (' ' SPACE)
        s = s.replace(u"\u2000", u"\u0020") # EN QUAD
        s = s.replace(u"\u2001", u"\u0020") # EM QUAD
        s = s.replace(u"\u2002", u"\u0020") # EN SPACE
        s = s.replace(u"\u2003", u"\u0020") # EM SPACE
        s = s.replace(u"\u2004", u"\u0020") # THREE-PER-EM SPACE
        s = s.replace(u"\u2005", u"\u0020") # FOUR-PER-EM SPACE
        s = s.replace(u"\u2006", u"\u0020") # SIX-PER-EM SPACE
        s = s.replace(u"\u2007", u"\u0020") # FIGURE SPACE
        s = s.replace(u"\u2008", u"\u0020") # PUNCTUATION SPACE
        s = s.replace(u"\u2009", u"\u0020") # THIN SPACE
        s = s.replace(u"\u200A", u"\u0020") # HAIR SPACE

        # linking
        s = s.replace(u"\u2040", u"\u203F") # CHARACTER TIE

        # global-rise
        s = s.replace(u"\u2191", u"\u2197") # UPWARDS ARROW

        # global-fall
        s = s.replace(u"\u2193", u"\u2198") # DOWNWARDS ARROW

        # major-group
        s = s.replace(u"\u2016", u"\u007C\u007c") # DOUBLE VERTICAL LINE

        # voiceless palato-alveolar sibilant-fricative consonant (LATIN SMALL LETTER ESH) 
        s = s.replace(u"\u222B", u"\u0283") # INTEGRAL

        # voiced palatal nasal consonant (LATIN SMALL LETTER N WITH LEFT HOOK)
        s = s.replace(u"\u00F1", u"\u0272") # LATIN SMALL LETTER N WITH TILDE

        # open-mid back rounded vowel (LATIN SMALL LETTER OPEN O)
        s = s.replace(u"\u1D10", u"\u0254") # LATIN LETTER SMALL CAPITAL OPEN O

        # open-mid front unrounded vowel (LATIN SMALL LETTER OPEN E)
        s = s.replace(u"\u03B5", u"\u025B") # GREEK SMALL LETTER EPSILON
        s = s.replace(u"\u03AD", u"\u025B") # GREEK SMALL LETTER EPSILON WITH TONOS

        # mid central unrounded vowel (LATIN SMALL LETTER SCHWA)
        s = s.replace(u"\u01DD", u"\u0259") # LATIN SMALL LETTER TURNED E

        # close-mid back unrounded vowel (LATIN SMALL LETTER RAMS HORN)
        s = s.replace(u"\u03B3", u"\u0264") # GREEK SMALL LETTER GAMMA

        # voiced dental non-sibilant-fricative consonant (LATIN SMALL LETTER ETH)
        s = s.replace(u"\u03B4", u"\u00F0") # GREEK SMALL LETTER DELTA

        # remove grave/acute/circumflex/tilde/diaeresis/macron/caron
        s = s.replace(u"\u00E0", u"a") # LATIN SMALL LETTER A WITH GRAVE
        s = s.replace(u"\u00E1", u"a") # LATIN SMALL LETTER A WITH ACUTE
        s = s.replace(u"\u00E2", u"a") # LATIN SMALL LETTER A WITH CIRCUMFLEX
        s = s.replace(u"\u00E3", u"a") # LATIN SMALL LETTER A WITH TILDE
        s = s.replace(u"\u00E4", u"a") # LATIN SMALL LETTER A WITH DIAERESIS
        
        s = s.replace(u"\u00E8", u"e") # LATIN SMALL LETTER E WITH GRAVE
        s = s.replace(u"\u00E9", u"e") # LATIN SMALL LETTER E WITH ACUTE
        s = s.replace(u"\u00EA", u"e") # LATIN SMALL LETTER E WITH CIRCUMFLEX
        s = s.replace(u"\u00EB", u"e") # LATIN SMALL LETTER E WITH DIAERESIS
        
        s = s.replace(u"\u00EC", u"i") # LATIN SMALL LETTER I WITH GRAVE
        s = s.replace(u"\u00ED", u"i") # LATIN SMALL LETTER I WITH ACUTE
        s = s.replace(u"\u00EE", u"i") # LATIN SMALL LETTER I WITH CIRCUMFLEX
        s = s.replace(u"\u00EF", u"i") # LATIN SMALL LETTER I WITH DIAERESIS
        
        s = s.replace(u"\u00F2", u"o") # LATIN SMALL LETTER O WITH GRAVE
        s = s.replace(u"\u00F3", u"o") # LATIN SMALL LETTER O WITH ACUTE
        s = s.replace(u"\u00F4", u"o") # LATIN SMALL LETTER O WITH CIRCUMFLEX
        s = s.replace(u"\u00F5", u"o") # LATIN SMALL LETTER O WITH TILDE
        s = s.replace(u"\u00F6", u"o") # LATIN SMALL LETTER O WITH DIAERESIS

        s = s.replace(u"\u00F9", u"u") # LATIN SMALL LETTER O WITH GRAVE
        s = s.replace(u"\u00FA", u"u") # LATIN SMALL LETTER O WITH ACUTE
        s = s.replace(u"\u00FB", u"u") # LATIN SMALL LETTER O WITH CIRCUMFLEX
        s = s.replace(u"\u00FC", u"u") # LATIN SMALL LETTER O WITH DIAERESIS

        s = s.replace(u"\u0101", u"a") # LATIN SMALL LETTER A WITH MACRON
        s = s.replace(u"\u0103", u"a") # LATIN SMALL LETTER A WITH BREVE
        s = s.replace(u"\u0113", u"e") # LATIN SMALL LETTER E WITH MACRON
        s = s.replace(u"\u0115", u"e") # LATIN SMALL LETTER E WITH BREVE
        s = s.replace(u"\u1EA1", u"a") # LATIN SMALL LETTER A WITH DOT BELOW
        s = s.replace(u"\u1EBD", u"e") # LATIN SMALL LETTER E WITH TILDE
        s = s.replace(u"\u012B", u"i") # LATIN SMALL LETTER I WITH MACRON
        s = s.replace(u"\u012D", u"i") # LATIN SMALL LETTER I WITH BREVE
        s = s.replace(u"\u0129", u"i") # LATIN SMALL LETTER I WITH TILDE
        s = s.replace(u"\u0131", u"i") # LATIN SMALL LETTER DOTLESS I
        s = s.replace(u"\u01D0", u"i") # LATIN SMALL LETTER I WITH CARON
        s = s.replace(u"\u014D", u"o") # LATIN SMALL LETTER O WITH MACRON
        s = s.replace(u"\u014F", u"o") # LATIN SMALL LETTER O WITH BREVE
        s = s.replace(u"\u0169", u"u") # LATIN SMALL LETTER U WITH TILDE
        s = s.replace(u"\u016B", u"u") # LATIN SMALL LETTER U WITH MACRON
        s = s.replace(u"\u016D", u"u") # LATIN SMALL LETTER U WITH BREVE
        
        # remove
        s = s.replace(u"\u0021", u"") # EXCLAMATION MARK
        s = s.replace(u"\u0025", u"") # PERCENT SIGN
        s = s.replace(u"\u0026", u"") # AMPERSAND 
        s = s.replace(u"\u0028", u"") # LEFT PARENTHESIS
        s = s.replace(u"\u0029", u"") # RIGHT PARENTHESIS
        s = s.replace(u"\u002A", u"") # ASTERISK
        s = s.replace(u"\u002D", u"") # HYPHEN-MINUS
        s = s.replace(u"\u002F", u"") # SOLIDUS
        s = s.replace(u"\u003F", u"") # QUESTION MARK
        s = s.replace(u"\u005B", u"") # LEFT SQUARE BRACKET
        s = s.replace(u"\u005C", u"") # REVERSE SOLIDUS
        s = s.replace(u"\u005D", u"") # RIGHT SQUARE BRACKET
        s = s.replace(u"\u007B", u"") # LEFT CURLY BRACKET
        s = s.replace(u"\u007D", u"") # RIGHT CURLY BRACKET
        s = s.replace(u"\u00A0", u"") # NO-BREAK SPACE
        s = s.replace(u"\u00B0", u"") # DEGREE SIGN
        s = s.replace(u"\u02C9", u"") # MODIFIER LETTER MACRON 
        s = s.replace(u"\u02CD", u"") # MODIFIER LETTER LOW MACRON 
        s = s.replace(u"\u02D6", u"") # MODIFIER LETTER PLUS SIGN
        s = s.replace(u"\u030D", u"") # COMBINING VERTICAL LINE ABOVE
        s = s.replace(u"\u032D", u"") # COMBINING CIRCUMFLEX ACCENT BELOW
        s = s.replace(u"\u0326", u"") # COMBINING COMMA BELOW
        s = s.replace(u"\u0336", u"") # COMBINING LONG STROKE OVERLAY
        s = s.replace(u"\u0342", u"") # COMBINING GREEK PERISPOMENI
        s = s.replace(u"\u200B", u"") # ZERO WIDTH SPACE
        s = s.replace(u"\u200C", u"") # ZERO WIDTH NON-JOINER
        s = s.replace(u"\u200D", u"") # ZERO WIDTH JOINER
        s = s.replace(u"\u200E", u"") # LEFT-TO-RIGHT MARK MARK
        s = s.replace(u"\u200F", u"") # RIGHT-TO-LEFT MARK
        s = s.replace(u"\u2010", u"") # HYPHEN
        s = s.replace(u"\u2011", u"") # NON-BREAKING HYPHEN
        s = s.replace(u"\u2012", u"") # FIGURE DASH
        s = s.replace(u"\u2013", u"") # EN DASH
        s = s.replace(u"\u2014", u"") # EM DASH
        s = s.replace(u"\u2015", u"") # HORIZONTAL BAR
        s = s.replace(u"\u2026", u"") # HORIZONTAL ELLIPSIS
        s = s.replace(u"\u2060", u"") # WORD JOINER

        return s



