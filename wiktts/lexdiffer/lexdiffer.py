#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function
import os

from ipapy.ipastring import IPAString

from wiktts import write_file
from wiktts.commandlinetool import CommandLineTool
from wiktts.lexdiffer.sequencelexicon import SequenceLexicon
from wiktts.lexdiffer.comparator import Comparator 

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class LexDiffer(CommandLineTool):

    AP_PROGRAM = u"wiktts.lexdiffer"
    AP_DESCRIPTION = u"Compare pronunciation lexica."
    AP_ARGUMENTS = [
        {
            "name": "lexicon1",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "First lexicon file"
        },
        {
            "name": "lexicon2",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "Second lexicon file (reference)"
        },
        {
            "name": "--ipa",
            "action": "store_true",
            "help": "The input lexica contain IPA strings (not mapped)"
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
        {
            "name": "--stats",
            "action": "store_true",
            "help": "Print statistics"
        },
        {
            "name": "--stdout",
            "action": "store_true",
            "help": "Print results to standard output"
        },
    ]

    def __init__(
            self,
            lexicon1=None,
            lexicon2=None,
        ):
        super(LexDiffer, self).__init__()
        self.lexicon1 = lexicon1
        self.lexicon2 = lexicon2
        self.comparator = None

    def _create_lexica(self, lexicon1_file_path, lexicon2_file_path, ipa):
        def field_to_ipa(string):
            return IPAString(unicode_string=string).ipa_chars

        self.lexicon1 = SequenceLexicon()
        self.lexicon2 = SequenceLexicon()
        if ipa:
            self.lexicon1.read_file(
                lexicon_file_path=lexicon1_file_path,
                field_to_sequence_function=field_to_ipa
            )
            self.lexicon2.read_file(
                lexicon_file_path=lexicon2_file_path,
                field_to_sequence_function=field_to_ipa
            )
        else:
            self.lexicon1.read_file(lexicon_file_path=lexicon1_file_path)
            self.lexicon2.read_file(lexicon_file_path=lexicon2_file_path)
        self.comparator = Comparator(self.lexicon1, self.lexicon2)

    def actual_command(self):
        # get options
        lexicon1_file_path = self.vargs["lexicon1"]
        lexicon2_file_path = self.vargs["lexicon2"]
        
        # options to filter/format results
        ipa = self.vargs["ipa"]
        diff_only = self.vargs["diff_only"]
        sort = not self.vargs["no_sort"]
        color = not self.vargs["no_color"]

        # options controlling print behavior
        print_stats = self.vargs["stats"]
        print_stdout = self.vargs["stdout"]
        created_files = []

        # checks
        if not os.path.isfile(lexicon1_file_path):
            self.error(u"The first lexicon file must exist. (Got '%s')" % lexicon1_file_path)
        if not os.path.isfile(lexicon2_file_path):
            self.error(u"The second lexicon file must exist. (Got '%s')" % lexicon2_file_path)

        # load lexica and compare
        self._create_lexica(lexicon1_file_path, lexicon2_file_path, ipa)
        self.comparator.compare()

        # save to plain text file
        formatted_data = self.comparator.pretty_print(diff_only=diff_only, sort=sort, fmt=u"plain", color=False)
        created_files.append(lexicon1_file_path + u".diff")
        write_file(formatted_data, created_files[-1])

        # save to HTML file
        formatted_data = self.comparator.pretty_print(diff_only=diff_only, sort=sort, fmt=u"html", color=True)
        created_files.append(lexicon1_file_path + u".diff.html")
        write_file(formatted_data, created_files[-1])

        # print to stdout if requested 
        if print_stdout:
            formatted_data = self.comparator.pretty_print(diff_only=diff_only, sort=sort, fmt=u"plain", color=color)
            for d in formatted_data:
                self.print_stdout(d)

        # output stats
        stats = []
        stats.append(u"Lexicon 1 path:        %s" % lexicon1_file_path)
        stats.append(u"Lexicon 2 path:        %s" % lexicon2_file_path)
        stats.append(u"Diff only:             %s" % diff_only)
        stats.append(u"Sort:                  %s" % sort)
        stats.append(u"Color:                 %s" % color)
        stats.append(u"")
        stats.append(self.comparator.pretty_print_stats())
        created_files.append(lexicon1_file_path + u".diff_stats")
        write_file(stats, created_files[-1])

        # print statistics if requested
        for f in created_files:
            self.print_stderr("Created file: %s" % f)
        if print_stats:
            self.print_stderr(u"\n".join(stats))



def main():
    LexDiffer().run()

if __name__ == "__main__":
    main()



