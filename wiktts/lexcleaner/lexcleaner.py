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
from wiktts.cleanedpronunciationlexicon import CleanedPronunciationLexicon
from wiktts.commandlinetool import CommandLineTool
from wiktts.lexcleaner.pronunciationcleaner import PronunciationCleaner
from wiktts.lexcleaner.unicodecleaner import UnicodeCleaner

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
            "name": "--chars",
            "nargs": "?",
            "type": str,
            "default": u"all",
            "help": "Map only the specified IPA characters [%s] (default: 'all')" % u"|".join(CleanedPronunciationLexicon.FILTER_IPA_CHARS)
        },
        {
            "name": "--word-cleaner",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Apply replacements from the given file to words"
        },
        {
            "name": "--pron-cleaner",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Apply replacements from the given file to pronunciation strings"
        },
        {
            "name": "--format",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Format output according to this template (available placeholders: %s)" % ", ".join(CleanedPronunciationLexicon.PLACEHOLDERS)
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
            "name": "--pron-index",
            "nargs": "?",
            "type": int,
            "default": 1,
            "help": "Field index of the pronunciation (default: 1)"
        },
        {
            "name": "--lowercase",
            "action": "store_true",
            "help": "Lowercase all the words"
        },
        {
            "name": "--comment-invalid",
            "action": "store_true",
            "help": "Comment lines containing words with invalid IPA pronunciation (after cleaning; you might want --no-sort as well)"
        },
        {
            "name": "--all",
            "action": "store_true",
            "help": "Print results for all words (with or without valid IPA pronunciation after cleaning)"
        },
        {
            "name": "--invalid",
            "action": "store_true",
            "help": "Print results for words with invalid IPA pronunciation (after cleaning)"
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

    def _create_lexicon(self, lexicon_file_path, comment, delimiter, word_index, pron_index, word_cleaner_path, pron_cleaner_path, lowercase, chars):
        word_cleaner = None if word_cleaner_path is None else UnicodeCleaner(word_cleaner_path, lowercase=lowercase)
        pron_cleaner = PronunciationCleaner() if pron_cleaner_path is None else UnicodeCleaner(pron_cleaner_path)
        self.lexicon = CleanedPronunciationLexicon(lowercase=lowercase)
        self.lexicon.read_file(
            lexicon_file_path=lexicon_file_path,
            comment=comment,
            delimiter=delimiter,
            indices=[word_index, pron_index]
        )
        self.lexicon.apply_cleaner(word_cleaner=word_cleaner, pron_cleaner=pron_cleaner)
        self.lexicon.filter_chars(chars=chars)

    def actual_command(self):
        # options to init the object
        self.output_directory_path = self.vargs["outputdir"]
        lexicon_file_path = self.vargs["lexicon"]
        word_cleaner_path = self.vargs["word_cleaner"]
        pron_cleaner_path = self.vargs["pron_cleaner"]
        comment = self.vargs["comment"]
        delimiter = self.vargs["delimiter"]
        word_index = self.vargs["word_index"]
        pron_index = self.vargs["pron_index"] 
        
        # options to filter/format results
        lowercase = self.vargs["lowercase"]
        chars = self.vargs["chars"]
        comment_invalid = self.vargs["comment_invalid"]
        template = self.vargs["format"]
        sort = not self.vargs["no_sort"]
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
        if (pron_cleaner_path is not None) and (not os.path.isfile(pron_cleaner_path)):
            self.error(u"The pronunciation cleaner source file must exist. (Got '%s')" % pron_cleaner_path)
        base = os.path.basename(lexicon_file_path)
        
        # load lexicon
        self._create_lexicon(
            lexicon_file_path,
            comment,
            delimiter,
            word_index,
            pron_index,
            word_cleaner_path,
            pron_cleaner_path,
            lowercase,
            chars
        )
        
        # filter/format data
        if select_all:
            include_valid, include_invalid = (True, True)
        elif select_invalid:
            include_valid, include_invalid = (False, True)
        else:
            include_valid, include_invalid = (True, False) 
        self.lexicon.select_entries(include_valid=include_valid, include_invalid=include_invalid)
        formatted_data = self.lexicon.format_lexicon(
            template=template,
            comment_invalid=comment_invalid,
            comment=comment,
            sort=sort
        )

        # output as requested
        created_files.append(os.path.join(self.output_directory_path, base + u".clean"))
        write_file(formatted_data, created_files[-1]) 

        created_files.append(os.path.join(self.output_directory_path, base + u".letters"))
        write_file(self.lexicon.format_letters(), created_files[-1])
        
        created_files.append(os.path.join(self.output_directory_path, base + u".phones"))
        write_file(self.lexicon.format_phones(), created_files[-1])

        # output stats
        stats = []
        stats.append(u"Lexicon path:          %s" % lexicon_file_path)
        stats.append(u"Output directory:      %s" % self.output_directory_path)
        stats.append(u"Word cleaner:          %s" % word_cleaner_path)
        stats.append(u"Pronunciation cleaner: %s" % pron_cleaner_path)
        stats.append(u"Lowercase word:        %s" % lowercase)
        stats.append(u"Sort words:            %s" % sort)
        stats.append(u"Include valid:         %s" % include_valid)
        stats.append(u"Include invalid:       %s" % include_invalid)
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



