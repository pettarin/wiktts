#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import division 
from __future__ import print_function

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

ANSI_RED = u"\033[91m"
ANSI_GREEN = u"\033[92m"
ANSI_YELLOW = u"\033[93m"
ANSI_NORMAL = u"\033[0m"

class ComparisonResult(object):

    def __init__(self, word, equal, l1, l2, ops):
        self.word = word
        self.equal = equal
        self.l1 = l1
        self.l2 = l2
        self.ops = ops
        self.__matches = 0
        self.__edits = 0
        self.__additions = 0
        self.__deletions = 0
        for op in ops:
            if op[0] == "m":
                self.__matches += 1
            elif op[0] == "a":
                self.__additions += 1
            elif op[0] == "d":
                self.__deletions += 1
            else:
                self.__edits += 1

    @property
    def matches(self):
        return self.__matches

    @property
    def nonmatches(self):
        return self.__edits + self.__additions + self.__deletions

    @property
    def edits(self):
        return self.__edits

    @property
    def additions(self):
        return self.__additions

    @property
    def deletions(self):
        return self.__deletions

    def pretty_print(self, fmt=u"plain", color=True):
        acc = []
        if fmt == u"plain":
            m_pre = ANSI_NORMAL if color else u""
            m_post = ANSI_NORMAL if color else u""
            a_pre = ANSI_GREEN if color else u"+"
            a_post = ANSI_NORMAL if color else u""
            d_pre = ANSI_RED if color else u"-"
            d_post = ANSI_NORMAL if color else u""
            e_pre = ANSI_YELLOW if color else u"/"
            e_post = ANSI_NORMAL if color else u""
        else:
            m_pre = u"<span class=\"m\">"
            m_post = u"</span>"
            a_pre = u"<span class=\"a\">"
            a_post = u"</span>"
            d_pre = u"<span class=\"d\">"
            d_post = u"</span>"
            e_pre = u"<span class=\"e\">"
            e_post = u"</span>"
        for op in self.ops:
            if op[0] == "m":
                acc.append(u"%s%s%s" % (m_pre, op[1], m_post))
            elif op[0] == "a":
                acc.append(u"%s%s%s" % (a_pre, op[1], a_post))
            elif op[0] == "d":
                acc.append(u"%s%s%s" % (d_pre, op[1], d_post))
            else:
                acc.append(u"%s%s/%s%s" % (e_pre, op[1], op[2], e_post))
        if fmt == u"plain":
            return u"%s\t%s" % (self.word, u" ".join(acc))
        elif fmt == u"html":
            return u"<tr><td>%s</td><td>%s</td></tr>" % (self.word, u" ".join(acc))
        return u""



class Comparator(object):
    """
    TBW
    """

    def __init__(self, lexicon1, lexicon2):
        self.lexicon1 = lexicon1
        self.lexicon2 = lexicon2
        self.stats = dict()
        self.comparisons = dict()

    @property
    def words_in_common(self):
        return self.words(in_lexicon1=True, in_lexicon2=True)

    def words(self, in_lexicon1, in_lexicon2):
        if in_lexicon1 and in_lexicon2:
            return set(self.lexicon1.words) & set(self.lexicon2.words)
        if in_lexicon1 and not in_lexicon2:
            return set(self.lexicon1.words) - set(self.lexicon2.words)
        if in_lexicon2 and not in_lexicon1:
            return set(self.lexicon2.words) - set(self.lexicon1.words)
        return set() 

    def compare_sequences(self, word, p1, p2):
        # shortcut if they are equal
        if p1 == p2:
            return ComparisonResult(word, True, len(p1), len(p2), [("m", p) for p in p1])
        # fill edit distance matrix
        matrix = [[0 for j in range(1 + len(p2))] for i in range(1 + len(p1))]
        for i in range(1 + len(p1)):
            matrix[i][0] = (i, "d")
        for j in range(1 + len(p2)):
            matrix[0][j] = (j, "a")
        for i in range(1, 1 + len(p1)):
            for j in range(1, 1 + len(p2)):
                if p1[i-1] == p2[j-1]:
                    matrix[i][j] = (matrix[i-1][j-1][0], "m")
                else:
                    d = matrix[i-1][j][0]
                    a = matrix[i][j-1][0]
                    m = matrix[i-1][j-1][0]
                    if (m <= d) and (m <= a):
                        matrix[i][j] = (1 + matrix[i-1][j-1][0], "e")
                    elif (d <= m) and (d <= a):
                        matrix[i][j] = (1 + matrix[i-1][j][0], "d")
                    else:
                        matrix[i][j] = (1 + matrix[i][j-1][0], "a")
        # create edit sequence by backtracking
        ops = []
        i = len(p1)
        j = len(p2)
        while (i > 0) or (j > 0):
            op = matrix[i][j][1]
            if op == "m":
                ops.append((op, p1[i-1]))
                i -= 1
                j -= 1
            elif op == "a":
                ops.append((op, p2[j-1]))
                j -= 1
            elif op == "d":
                ops.append((op, p1[i-1]))
                i -= 1
            else:
                ops.append((op, p1[i-1], p2[j-1]))
                i -= 1
                j -= 1
        return ComparisonResult(word, False, len(p1), len(p2), ops[::-1])

    def compare(self, compare_first_only=True):
        common = self.words_in_common
        sta = dict()
        com = dict()
        sta[u"size_lexicon1"] = len(self.lexicon1)
        sta[u"size_lexicon2"] = len(self.lexicon2)
        sta[u"size_common"] = len(common)
        sta[u"phones1"] = 0
        sta[u"phones2"] = 0
        sta[u"seq_correct"] = 0
        sta[u"seq_incorrect"] = 0
        sta[u"phones_correct"] = 0
        sta[u"phones_incorrect"] = 0
        sta[u"phones_matches"] = 0
        sta[u"phones_edits"] = 0
        sta[u"phones_additions"] = 0
        sta[u"phones_deletions"] = 0
        for w in common:
            e1 = self.lexicon1.entries_for_word(w)
            e2 = self.lexicon2.entries_for_word(w)
            if compare_first_only:
                r = self.compare_sequences(w, e1[0].phones, e2[0].phones)
                sta[u"phones1"] += r.l1
                sta[u"phones2"] += r.l2
                sta[u"phones_correct"] += r.matches
                if r.equal:
                    sta[u"seq_correct"] += 1
                else:
                    sta[u"seq_incorrect"] += 1
                    sta[u"phones_incorrect"] += r.nonmatches
                com[w] = r
                sta[u"phones_matches"] += r.matches
                sta[u"phones_edits"] += r.edits
                sta[u"phones_additions"] += r.additions
                sta[u"phones_deletions"] += r.deletions
            else:
                # TODO
                pass
        self.stats = sta
        self.comparisons = com

    def pretty_print(self, diff_only=False, sort=False, fmt=u"plain", color=False):
        acc = []
        if fmt == u"html":
            acc.append(u"<!DOCTYPE html>")
            acc.append(u"<html>")
            acc.append(u" <head>")
            acc.append(u"  <meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">")
            acc.append(u"  <meta charset=\"utf-8\">")
            acc.append(u" <style>")
            acc.append(u"  body { background: black; color: white; font-size: 16px; font-family: monospace; }")
            acc.append(u"  .m { color: white; }")
            acc.append(u"  .a { color: green; }")
            acc.append(u"  .d { color: red; }")
            acc.append(u"  .e { color: yellow; }")
            acc.append(u" </style>")
            acc.append(u" </head>")
            acc.append(u" <body>")
            acc.append(u"  <table>")
        
        words = self.comparisons.keys()
        if sort:
            words = sorted(words)
        else:
            words = [w for w in self.lexicon1.words if w in self.words_in_common]
        for w in words:
            c = self.comparisons[w]
            if (not diff_only) or (not c.equal):
                acc.append(c.pretty_print(fmt=fmt, color=color))
        
        if fmt == u"html":
            acc.append(u"  </table>")
            acc.append(u" </body>")
            acc.append(u"</html>")
        return acc

    def pretty_print_stats(self):
        stats = []
        stats.append(u"Entries in lexicon 1:  %d" % self.stats[u"size_lexicon1"])
        stats.append(u"Entries in lexicon 2:  %d" % self.stats[u"size_lexicon2"])
        stats.append(u"")
        stats.append(u"Entries in common:     %d" % self.stats[u"size_common"])
        if self.stats[u"size_common"] > 0:
            stats.append(u"  Correct sequences:   %d (%.3f%%)" % (self.stats[u"seq_correct"], 100 * self.stats[u"seq_correct"] / self.stats[u"size_common"]))
            stats.append(u"  Incorrect sequences: %d (%.3f%%)" % (self.stats[u"seq_incorrect"], 100 * self.stats[u"seq_incorrect"] / self.stats[u"size_common"]))
            stats.append(u"  Correct phones:      %d (%.3f%%)" % (self.stats[u"phones_correct"], 100 * self.stats[u"phones_correct"] / self.stats[u"phones1"]))
            stats.append(u"  Incorrect phones:    %d (%.3f%%)" % (self.stats[u"phones_incorrect"], 100 * self.stats[u"phones_incorrect"] / self.stats[u"phones1"]))
            #stats.append(u"    Matches:           %d (%.3f%%)" % (self.stats[u"phones_matches"], 100 * self.stats[u"phones_matches"] / self.stats[u"phones1"]))
            stats.append(u"    Edits:             %d (%.3f%%)" % (self.stats[u"phones_edits"], 100 * self.stats[u"phones_edits"] / self.stats[u"phones1"]))
            stats.append(u"    Additions:         %d (%.3f%%)" % (self.stats[u"phones_additions"], 100 * self.stats[u"phones_additions"] / self.stats[u"phones1"]))
            stats.append(u"    Deletions:         %d (%.3f%%)" % (self.stats[u"phones_deletions"], 100 * self.stats[u"phones_deletions"] / self.stats[u"phones1"]))
        return u"\n".join(stats)



