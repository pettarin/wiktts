#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import division 
from __future__ import print_function
import os

from wiktts import write_file
from wiktts.commandlinetool import CommandLineTool
from wiktts.lexdiffer.sequencelexicon import SequenceLexicon
from wiktts.lexdiffer.comparator import Comparator 

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class LexDiffer(CommandLineTool):

    AP_DESCRIPTION = u"Compare pronunciation lexica."
    AP_ARGUMENTS = [
        {
            "name": "lexicon1",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "First lexicon"
        },
        {
            "name": "lexicon2",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "First lexicon"
        },
        {
            "name": "--comment",
            "nargs": "?",
            "type": str,
            "default": u"#",
            "help": "Ignore lines in the lexicon file starting with this string (default: '#')"
        },
        {
            "name": "--delimiter",
            "nargs": "?",
            "type": str,
            "default": "\t",
            "help": "Field delimiter of the lexicon file (default: '\\t')"
        },
        {
            "name": "--phones-delimiter",
            "nargs": "?",
            "type": str,
            "default": " ",
            "help": "Phone delimiter of the lexicon file (default: ' ')"
        },
        {
            "name": "--word-index1",
            "nargs": "?",
            "type": int,
            "default": 0,
            "help": "Field index of the word in the first lexicon file (default: 0)"
        },
        {
            "name": "--phones-index1",
            "nargs": "?",
            "type": int,
            "default": 1,
            "help": "Field index of the phones in the first lexicon file (default: 1)"
        },
        {
            "name": "--word-index2",
            "nargs": "?",
            "type": int,
            "default": 0,
            "help": "Field index of the word in the second lexicon file (default: 0)"
        },
        {
            "name": "--phones-index2",
            "nargs": "?",
            "type": int,
            "default": 1,
            "help": "Field index of the phones in the second lexicon file (default: 1)"
        },
        {
            "name": "--quiet",
            "action": "store_true",
            "help": "Do not print results to stdout"
        },
        {
            "name": "--stats",
            "action": "store_true",
            "help": "Print statistics"
        },
        {
            "name": "--no-color",
            "action": "store_true",
            "help": "Do not color output"
        },
    ]

    def actual_command(self):
        # get options
        lexicon1_file_path = self.vargs["lexicon1"]
        lexicon2_file_path = self.vargs["lexicon2"]
        quiet = self.vargs["quiet"]
        print_stats = self.vargs["stats"] 
        comment = self.vargs["comment"]
        delimiter = self.vargs["delimiter"]
        phones_delimiter = self.vargs["phones_delimiter"]
        word_index1 = self.vargs["word_index1"]
        phones_index1 = self.vargs["phones_index1"]
        word_index2 = self.vargs["word_index2"]
        phones_index2 = self.vargs["phones_index2"]
        color = not self.vargs["no_color"]

        lexicon1 = SequenceLexicon()
        lexicon1.read_file(
            lexicon_file_path=lexicon1_file_path,
            comment=comment,
            delimiter=delimiter,
            phones_delimiter=phones_delimiter,
            word_index=word_index1,
            phones_index=phones_index1
        )

        lexicon2 = SequenceLexicon()
        lexicon2.read_file(
            lexicon_file_path=lexicon2_file_path,
            comment=comment,
            delimiter=delimiter,
            phones_delimiter=phones_delimiter,
            word_index=word_index2,
            phones_index=phones_index2
        )

        res = Comparator(lexicon1, lexicon2).compare()

        if not quiet:
            c = res["comparisons"]
            for k in c:
                if not c[k].equal:
                    print("%s\t%s" % (k, c[k].pretty_print(color=color)))

        if print_stats:
            print(u"Entries in lexicon 1: %d" % res[u"size_lexicon1"])
            print(u"Entries in lexicon 2: %d" % res[u"size_lexicon2"])
            print(u"Entries in common:    %d" % res[u"size_common"])
            print(u"Correct sequences:    %d (%.3f%%)" % (res[u"seq_correct"], 100 * res[u"seq_correct"] / res[u"size_common"]))
            print(u"Incorrect sequences:  %d (%.3f%%)" % (res[u"seq_incorrect"], 100 * res[u"seq_incorrect"] / res[u"size_common"]))
            print(u"Correct phones:       %d (%.3f%%)" % (res[u"phones_correct"], 100 * res[u"phones_correct"] / res[u"phones1"]))
            print(u"Incorrect phones:     %d (%.3f%%)" % (res[u"phones_incorrect"], 100 * res[u"phones_incorrect"] / res[u"phones1"]))
            print(u"Phone matches:        %d (%.3f%%)" % (res[u"phones_matches"], 100 * res[u"phones_matches"] / res[u"phones1"]))
            print(u"Phone edits:          %d (%.3f%%)" % (res[u"phones_edits"], 100 * res[u"phones_edits"] / res[u"phones1"]))
            print(u"Phone additions:      %d (%.3f%%)" % (res[u"phones_additions"], 100 * res[u"phones_additions"] / res[u"phones1"]))
            print(u"Phone deletions:      %d (%.3f%%)" % (res[u"phones_deletions"], 100 * res[u"phones_deletions"] / res[u"phones1"]))







def main():
    LexDiffer().run()

if __name__ == "__main__":
    main()



