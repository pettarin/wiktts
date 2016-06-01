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

    AP_PROGRAM = u"wiktts.lexcleaner"
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
            "name": "outputdir",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "Output files in this directory"
        },
        {
            "name": "--word-cleaner",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Apply replacements from the given file to words"
        },
        {
            "name": "--ipa-cleaner",
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
            "name": "--lowercase",
            "action": "store_true",
            "help": "Lowercase all the words"
        },
        {
            "name": "--comment-invalid",
            "action": "store_true",
            "help": "Comment lines containing words with invalid IPA (after cleaning; you might want --no-sort as well)"
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
            lexicon=None,
            output_directory_path=None,
        ):
        super(LexCleaner, self).__init__()
        self.lexicon = lexicon
        self.output_directory_path = output_directory_path

    @property
    def output_directory_path(self):
        return self.__output_directory_path
    @output_directory_path.setter
    def output_directory_path(self, value):
        if value is not None:
            if not os.path.isdir(value):
                self.error("The output directory must exist. (Got: '%s')" % value)
        self.__output_directory_path = value

    def _create_lexicon(self, lexicon_file_path, comment, delimiter, word_index, ipa_index, word_cleaner_path, ipa_cleaner_path, lowercase):
        if word_cleaner_path is None:
            word_cleaner = DefaultWordCleaner(lowercase=lowercase)
        else:
            word_cleaner = UniCleaner(word_cleaner_path, lowercase=lowercase)
        if ipa_cleaner_path is None:
            ipa_cleaner = DefaultIPACleaner()
        else:
            ipa_cleaner = UniCleaner(ipa_cleaner_path)
        self.lexicon = Lexicon(
            word_cleaner=word_cleaner,
            ipa_cleaner=ipa_cleaner,
        )
        self.lexicon.read_file(
            lexicon_file_path=lexicon_file_path,
            comment=comment,
            delimiter=delimiter,
            word_index=word_index,
            ipa_index=ipa_index
        )

    def actual_command(self):
        # options to init the object
        self.output_directory_path = self.vargs["outputdir"]
        lexicon_file_path = self.vargs["lexicon"]
        word_cleaner_path = self.vargs["word_cleaner"]
        ipa_cleaner_path = self.vargs["ipa_cleaner"]
        lowercase = self.vargs["lowercase"]
        comment = self.vargs["comment"]
        delimiter = self.vargs["delimiter"]
        word_index = self.vargs["word_index"]
        ipa_index = self.vargs["ipa_index"] 
        
        # options to filter/format results
        comment_invalid = self.vargs["comment_invalid"]
        template = self.vargs["format"]
        sort_results = not self.vargs["no_sort"]
        select_all = self.vargs["all"]
        select_invalid = self.vargs["invalid"]
       
        # options controlling print behavior
        print_stats = self.vargs["stats"]
        print_stdout = self.vargs["stdout"]
        created_files = []

        # checks
        if not os.path.isfile(lexicon_file_path):
            self.error(u"The lexicon file must exist. (Got '%s')" % lexicon_file_path)
        if (word_cleaner_path is not None) and (not os.path.isfile(word_cleaner_path)):
            self.error(u"The word cleaner source file must exist. (Got '%s')" % word_cleaner_path)
        if (ipa_cleaner_path is not None) and (not os.path.isfile(ipa_cleaner_path)):
            self.error(u"The ipa cleaner source file must exist. (Got '%s')" % ipa_cleaner_path)
        base = os.path.basename(lexicon_file_path)
        
        # load lexicon
        self._create_lexicon(lexicon_file_path, comment, delimiter, word_index, ipa_index, word_cleaner_path, ipa_cleaner_path, lowercase)
        
        # filter/format data
        if select_all:
            self.lexicon.select_entries(include_valid=True, include_invalid=True)
        elif select_invalid:
            self.lexicon.select_entries(include_valid=False, include_invalid=True)
        else:
            self.lexicon.select_entries(include_valid=True, include_invalid=False)
        formatted_data = self.lexicon.format_lexicon(
            template=template,
            comment_invalid=comment_invalid,
            comment=comment
        )
        # sort if requested
        if sort_results:
            formatted_data = sorted(formatted_data)

        # output as requested
        created_files.append(os.path.join(self.output_directory_path, base + u".clean"))
        write_file(formatted_data, created_files[-1]) 

        created_files.append(os.path.join(self.output_directory_path, base + u".letters"))
        write_file(self.lexicon.format_letters(), created_files[-1])
        
        created_files.append(os.path.join(self.output_directory_path, base + u".phones"))
        write_file(self.lexicon.format_phones(), created_files[-1])

        # output stats
        stats = []
        stats.append(u"Lexicon path:     %s" % lexicon_file_path)
        stats.append(u"Output directory: %s" % self.output_directory_path)
        stats.append(u"Word cleaner:     %s" % word_cleaner_path)
        stats.append(u"IPA cleaner:      %s" % ipa_cleaner_path)
        stats.append(self.lexicon.pretty_print_stats())
        created_files.append(os.path.join(self.output_directory_path, base + u".cleaner_stats"))
        write_file(stats, created_files[-1])

        # print to stdout if requested 
        if print_stdout:
            for d in formatted_data:
                self.print_stdout(d)

        # print statistics if requested
        for f in created_files:
            self.print_stderr("Created file: %s" % f)
        if print_stats:
            self.print_stderr(u"\n".join(stats))



def main():
    LexCleaner().run()

if __name__ == "__main__":
    main()



