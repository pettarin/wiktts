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
from wiktts.lexicon import PLACEHOLDERS
from wiktts.lexicon import Lexicon
from wiktts.lexcleaner.unicleaner import UniCleaner
from wiktts.lexcleaner.unicleaner import DefaultWordCleaner
from wiktts.lexcleaner.unicleaner import DefaultIPACleaner

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class LexCleaner(CommandLineTool):

    AP_DESCRIPTION = u"Clean and normalize a pronunciation lexicon."
    AP_ARGUMENTS = [
        {
            "name": "lexicon",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "Input lexicon file"
        },
        {
            "name": "--output-file",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Write output to file"
        },
        {
            "name": "--letter-file",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Write list of symbols (in words) to file"
        },
        {
            "name": "--phone-file",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Write list of symbols (in IPA strings) to file"
        },
        {
            "name": "--word-cleaner-file",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Apply replacements from the given file to words"
        },
        {
            "name": "--ipa-cleaner-file",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Apply replacements from the given file to IPA strings"
        },
        {
            "name": "--format",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Format output according to this template (available placeholders: %s)" % ", ".join(PLACEHOLDERS)
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
            "name": "--no-sort",
            "action": "store_true",
            "help": "Do not sort the results"
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
            "name": "--all",
            "action": "store_true",
            "help": "Print results for all words (with or without valid IPA after cleaning)"
        },
        {
            "name": "--comment-invalid",
            "action": "store_true",
            "help": "Comment lines regarding words with invalid IPA (after cleaning; you might want --no-sort as well)"
        },
        {
            "name": "--invalid",
            "action": "store_true",
            "help": "Print results for words with invalid IPA (after cleaning)"
        },
        {
            "name": "--all-phones",
            "action": "store_true",
            "help": "Output all phones in the input lexicon, not just those selected by --format"
        },
    ]

    def actual_command(self):
        # get options
        lexicon = self.vargs["lexicon"]
        output_file_path = self.vargs["output_file"]
        letter_file_path = self.vargs["letter_file"]
        phone_file_path = self.vargs["phone_file"]
        word_cleaner_path = self.vargs["word_cleaner_file"]
        ipa_cleaner_path = self.vargs["ipa_cleaner_file"]
        all_phones = self.vargs["all_phones"]
        quiet = self.vargs["quiet"]
        print_stats = self.vargs["stats"] 
        sort_results = not self.vargs["no_sort"]
        template = self.vargs["format"]
        comment = self.vargs["comment"]
        comment_invalid = self.vargs["comment_invalid"]
        delimiter = self.vargs["delimiter"]
        word_index = self.vargs["word_index"]
        ipa_index = self.vargs["ipa_index"]

        # load cleaner
        if word_cleaner_path is None:
            word_cleaner = DefaultWordCleaner()
        else:
            word_cleaner = UniCleaner(word_cleaner_path)
        if ipa_cleaner_path is None:
            ipa_cleaner = DefaultIPACleaner()
        else:
            ipa_cleaner = UniCleaner(ipa_cleaner)

        # read lexicon and clean raw IPA strings
        lexi = Lexicon(
            clean=False,
            word_cleaner=word_cleaner,
            ipa_cleaner=ipa_cleaner,
        )
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
                include_invalid=include_invalid,
                comment_invalid=comment_invalid,
                comment=comment
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

        # save letters to file
        if letter_file_path is not None:
            write_file(lexi.format_letters(), letter_file_path)

        # save phones to file
        if phone_file_path is not None:
            p_template = "{CIPA}" if all_phones else template
            write_file(lexi.format_phones(p_template), phone_file_path)

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
    LexCleaner().run()

if __name__ == "__main__":
    main()



