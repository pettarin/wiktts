#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import division 
from __future__ import print_function
import os
from ipapy.ipastring import IPAString

from wiktts import write_file
from wiktts.commandlinetool import CommandLineTool
from wiktts.ipacleaner.iclexicon import PLACEHOLDERS
from wiktts.ipacleaner.iclexicon import ICLexicon

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class IPACleaner(CommandLineTool):

    AP_DESCRIPTION = u"Clean and normalize IPA strings mined from a MediaWiki dump file."
    AP_ARGUMENTS = [
        {
            "name": "lexicon",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "Lexicon file"
        },
        {
            "name": "--output-file",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Write output to file"
        },
        {
            "name": "--format",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Format output according to this string (available placeholders: %s)" % ", ".join(PLACEHOLDERS)
        },
        {
            "name": "--comment",
            "nargs": "?",
            "type": str,
            "default": "u",
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
            "name": "--word-index",
            "nargs": "?",
            "type": int,
            "default": 0,
            "help": "Field index of the word (default: 0)"
        },
        {
            "name": "--ipa-index",
            "nargs": "?",
            "type": int,
            "default": 1,
            "help": "Field index of the IPA string (default: 1)"
        },
        {
            "name": "--sort",
            "action": "store_true",
            "help": "Sort the results"
        },
        {
            "name": "--quiet",
            "action": "store_true",
            "help": "Do not print results to stdout"
        },
        {
            "name": "--stats",
            "action": "store_true",
            "help": "Print the number of words with valid and invalid IPA"
        },
        {
            "name": "--all",
            "action": "store_true",
            "help": "Print results for all words (with or without valid IPA after cleaning)"
        },
        {
            "name": "--invalid",
            "action": "store_true",
            "help": "Print results for words with invalid IPA (after cleaning)"
        },
    ]

    def actual_command(self):
        # get options
        lexicon = self.vargs["lexicon"]
        output_file_path = self.vargs["output_file"]
        quiet = self.vargs["quiet"]
        print_stats = self.vargs["stats"] 
        sort_results = self.vargs["sort"]
        template = self.vargs["format"]
        comment = self.vargs["comment"]
        delimiter = self.vargs["delimiter"]
        word_index = self.vargs["word_index"]
        ipa_index = self.vargs["ipa_index"]

        # read lexicon and clean raw IPA strings
        lexi = ICLexicon()
        lexi.read_file(
            lexicon_file_path=lexicon,
            comment=comment,
            delimiter=delimiter,
            word_index=word_index,
            ipa_index=ipa_index
        )

        # format data if file or stdout output should be produced
        if (output_file_path is not None) or (not quiet):
            # select the data to include in the output 
            if self.vargs["all"]:
                include_valid = True
                include_invalid = True
            elif self.vargs["invalid"]:
                include_valid = False
                include_invalid = True
            else:
                include_valid = True
                include_invalid = False
            # format data
            formatted_data = lexi.format_lexicon(
                template=template,
                include_valid=include_valid,
                include_invalid=include_invalid
            )
            # sort if requested
            if sort_results:
                formatted_data = sorted(formatted_data)
            # output as requested
            if output_file_path is not None:
                write_file(formatted_data, output_file_path)
            if not quiet:
                for d in formatted_data:
                    print(d)
        
        # print statistics if requested
        if print_stats:
            total = len(lexi)
            rv = len(lexi.raw_valid)
            rv_perc = rv / total * 100
            cv = len(lexi.cleaned_valid)
            cv_perc = cv / total * 100
            print("Words")
            print("  Total:                     %d" % total)
            print("  Raw IPA Valid/Invalid:     %d / %d (%0.3f%s / %0.3f%s)" % (rv, total - rv, rv_perc, "%", 100.0 - rv_perc, "%"))
            print("  Cleaned IPA Valid/Invalid: %d / %d (%0.3f%s / %0.3f%s)" % (cv, total - cv, cv_perc, "%", 100.0 - cv_perc, "%"))



def main():
    IPACleaner().run()

if __name__ == "__main__":
    main()



