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

    def pretty_print(self, color=True, stats=False):
        acc = []
        a_pre = ANSI_GREEN if color else u"+"
        a_post = ANSI_NORMAL if color else u""
        d_pre = ANSI_RED if color else u"-"
        d_post = ANSI_NORMAL if color else u""
        e_pre = ANSI_YELLOW if color else u""
        e_post = ANSI_NORMAL if color else u""
        for op in self.ops:
            if op[0] == "m":
                acc.append(op[1])
            elif op[0] == "a":
                acc.append(a_pre + op[1] + a_post)
            elif op[0] == "d":
                acc.append(d_pre + op[1] + d_post)
            else:
                acc.append(e_pre + op[1] + "/" + op[2] + e_post)
        ret = u" ".join(acc)
        if stats:
            ret += u"\t(M %d, E %s, A %d, D %s)" % (self.matches, self.edits, self.additions, self.deletions)
        return ret 



class Comparator(object):
    """
    TBW
    """

    def __init__(self, lexicon1, lexicon2):
        self.lexicon1 = lexicon1
        self.lexicon2 = lexicon2

    @property
    def words_in_common(self):
        return self.words(in_lexicon1=True, in_lexicon2=True)

    def words(self, in_lexicon1, in_lexicon2):
        if in_lexicon1 and in_lexicon2:
            return self.lexicon1.words & self.lexicon2.words
        if in_lexicon1 and not in_lexicon2:
            return self.lexicon1.words - self.lexicon2.words
        if in_lexicon2 and not in_lexicon1:
            return self.lexicon2.words - self.lexicon1.words
        return set() 

    def compare_phones(self, word, p1, p2):
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
        res = dict()
        res[u"size_lexicon1"] = len(self.lexicon1)
        res[u"size_lexicon2"] = len(self.lexicon2)
        res[u"size_common"] = len(common)
        res[u"comparisons"] = dict()
        res[u"phones1"] = 0
        res[u"phones2"] = 0
        res[u"seq_correct"] = 0
        res[u"seq_incorrect"] = 0
        res[u"phones_correct"] = 0
        res[u"phones_incorrect"] = 0
        res[u"phones_matches"] = 0
        res[u"phones_edits"] = 0
        res[u"phones_additions"] = 0
        res[u"phones_deletions"] = 0
        for w in common:
            e1 = self.lexicon1.entries_for_word(w)
            e2 = self.lexicon2.entries_for_word(w)
            if compare_first_only:
                r = self.compare_phones(w, e1[0].phones, e2[0].phones)
                res[u"phones1"] += r.l1
                res[u"phones2"] += r.l2
                res[u"phones_correct"] += r.matches
                if r.equal:
                    res[u"seq_correct"] += 1
                else:
                    res[u"seq_incorrect"] += 1
                    res[u"phones_incorrect"] += r.nonmatches
                res[u"comparisons"][w] = r
                res[u"phones_matches"] += r.matches
                res[u"phones_edits"] += r.edits
                res[u"phones_additions"] += r.additions
                res[u"phones_deletions"] += r.deletions
            else:
                # TODO
                pass
        return res


