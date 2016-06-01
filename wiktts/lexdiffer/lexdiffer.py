#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import division 
from __future__ import print_function

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
            "name": "--output-file",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Write output to file"
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
        {
            "name": "--diff-only",
            "action": "store_true",
            "help": "Do not output common lines"
        },
        {
            "name": "--no-sort",
            "action": "store_true",
            "help": "Do not sort the results"
        },
    ]

    def actual_command(self):
        # get options
        lexicon1_file_path = self.vargs["lexicon1"]
        lexicon2_file_path = self.vargs["lexicon2"]
        output_file_path = self.vargs["output_file"]
        sort_results = not self.vargs["no_sort"]
        quiet = self.vargs["quiet"]
        print_stats = self.vargs["stats"] 
        color = not self.vargs["no_color"]
        diff_only = self.vargs["diff_only"]

        lexicon1 = SequenceLexicon()
        lexicon1.read_file(lexicon_file_path=lexicon1_file_path)

        lexicon2 = SequenceLexicon()
        lexicon2.read_file(lexicon_file_path=lexicon2_file_path)

        comparator = Comparator(lexicon1, lexicon2)
        result = comparator.compare()

        if (output_file_path is not None) or (not quiet):
            comparisons = list(result["comparisons"].values())
            if diff_only:
                comparisons = [c for c in comparisons if not c.equal]
            if output_file_path is not None:
                formatted_data = []
                for c in comparisons:
                    formatted_data.append(u"%s\t%s" % (c.word, c.pretty_print(color=False)))
                if sort_results:
                    formatted_data = sorted(formatted_data)
                write_file(formatted_data, output_file_path)
            if not quiet:
                formatted_data = []
                for c in comparisons:
                    formatted_data.append(u"%s\t%s" % (c.word, c.pretty_print(color=color)))
                if sort_results:
                    formatted_data = sorted(formatted_data)
                for f in formatted_data:
                    print(f)

        if print_stats:
            print(u"")
            print(u"Entries in lexicon 1:  %d" % result[u"size_lexicon1"])
            print(u"Entries in lexicon 2:  %d" % result[u"size_lexicon2"])
            print(u"")
            print(u"Entries in common:     %d" % result[u"size_common"])
            print(u"  Correct sequences:   %d (%.3f%%)" % (result[u"seq_correct"], 100 * result[u"seq_correct"] / result[u"size_common"]))
            print(u"  Incorrect sequences: %d (%.3f%%)" % (result[u"seq_incorrect"], 100 * result[u"seq_incorrect"] / result[u"size_common"]))
            print(u"  Correct phones:      %d (%.3f%%)" % (result[u"phones_correct"], 100 * result[u"phones_correct"] / result[u"phones1"]))
            print(u"  Incorrect phones:    %d (%.3f%%)" % (result[u"phones_incorrect"], 100 * result[u"phones_incorrect"] / result[u"phones1"]))
            #print(u"    Matches:           %d (%.3f%%)" % (result[u"phones_matches"], 100 * result[u"phones_matches"] / result[u"phones1"]))
            print(u"    Edits:             %d (%.3f%%)" % (result[u"phones_edits"], 100 * result[u"phones_edits"] / result[u"phones1"]))
            print(u"    Additions:         %d (%.3f%%)" % (result[u"phones_additions"], 100 * result[u"phones_additions"] / result[u"phones1"]))
            print(u"    Deletions:         %d (%.3f%%)" % (result[u"phones_deletions"], 100 * result[u"phones_deletions"] / result[u"phones1"]))
            print(u"")







def main():
    LexDiffer().run()

if __name__ == "__main__":
    main()



