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
from wiktts.trainer.tool import FILTER_IPA_CHARS
from wiktts.trainer.tool import TOOLS
from wiktts.trainer.tool import ToolPhonetisaurus
from wiktts.trainer.tool import ToolSequitur

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class Trainer(CommandLineTool):

    AP_DESCRIPTION = u"Prepare train/test/symbol files for ML tools."
    AP_ARGUMENTS = [
        {
            "name": "tool",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "ML tool [%s]" % u"|".join(TOOLS)
        },
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
            "help": "Write output files to this directory"
        },
        {
            "name": "--include-chars",
            "nargs": "?",
            "type": str,
            "default": u"cv",
            "help": "Include only the given IPA characters [%s] (default: 'cv')" % u"|".join(FILTER_IPA_CHARS)
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
            "name": "--train-size-int",
            "nargs": "?",
            "type": int,
            "default": None,
            "help": "Size of the train set, in words"
        },
        {
            "name": "--train-size-frac",
            "nargs": "?",
            "type": float,
            "default": 0.9,
            "help": "Size of the train set relative to valid lexicon size (default: 0.9)"
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
            "name": "--output-script-only",
            "action": "store_true",
            "help": "Only output the Bash script to run the ML tool"
        },
        {
            "name": "--output-script",
            "action": "store_true",
            "help": "Output the Bash script to run the ML tool"
        },
        {
            "name": "--script-parameters",
            "nargs": "?",
            "type": str,
            "default": u"",
            "help": "Parameters to configure the Bash script to run the ML tool"
        },
    ]

    def actual_command(self):
        # get options
        tool = self.vargs["tool"]
        lexicon = self.vargs["lexicon"]
        output_dir_path =  self.vargs["outputdir"]
        quiet = self.vargs["quiet"]
        print_stats = self.vargs["stats"] 
        comment = self.vargs["comment"]
        delimiter = self.vargs["delimiter"]
        word_index = self.vargs["word_index"]
        ipa_index = self.vargs["ipa_index"]
        train_size = self.vargs["train_size_frac"] if self.vargs["train_size_int"] is None else self.vargs["train_size_int"]
        include_chars = self.vargs["include_chars"]
        output_script = self.vargs["output_script"]
        output_script_only = self.vargs["output_script_only"]
        script_parameters = self.vargs["script_parameters"]

        # make sure
        if tool not in [u"phonetisaurus", u"sequitur"]:
            self.error("The available tools are: %s. (Got: '%s')" % (TOOLS, tool))

        # make sure output directory exists
        if not os.path.isdir(output_dir_path):
            # TODO create dir instead?
            self.error("The output directory does not exist! (Got: '%s')" % output_dir_path)

        # output file names
        base = os.path.join(output_dir_path, os.path.basename(lexicon))
        train_file_path = base + u".train"
        test_file_path = base + u".test"
        symb_file_path = base + u".symbols"
        script_file_path = None
        if tool == u"phonetisaurus":
            cls = ToolPhonetisaurus
        else:
            cls = ToolSequitur

        if not output_script_only:
            # read lexicon and clean raw IPA strings
            lexi = Lexicon(clean=True)
            lexi.read_file(
                lexicon_file_path=lexicon,
                comment=comment,
                delimiter=delimiter,
                word_index=word_index,
                ipa_index=ipa_index
            )
            # create training, test, and symbol sets
            tool_formatter = cls(
                lexicon=lexi,
                include_chars=include_chars,
                mapper_name=None,
                train_size=train_size
            )
            write_file(tool_formatter.format_train(), train_file_path)
            write_file(tool_formatter.format_test(), test_file_path)
            write_file(tool_formatter.format_symbol_set(), symb_file_path)
            # print statistics if requested
            if print_stats:
                total = len(lexi)
                print("Words:")
                print("  Total: %d" % (tool_formatter.train_size + tool_formatter.test_size))
                print("  Train: %d" % tool_formatter.train_size)
                print("  Test:  %d" % tool_formatter.test_size)
                print("Symbols:")
                print("  Total: %d" % (tool_formatter.symbol_set_size))
                print("  Train: %d" % (tool_formatter.train_symbol_set_size))
                print("  Test:  %d" % (tool_formatter.test_symbol_set_size))
            if not quiet:
                print("Created file: %s" % train_file_path)
                print("Created file: %s" % test_file_path)
                print("Created file: %s" % symb_file_path)

        if output_script or output_script_only:
            parameters = {
                "base": os.path.basename(base),
                "sequitur_devel": "5",
                "sequitur_maxlevel": "8"
            }
            for p in script_parameters.split(u","):
                try:
                    k, v = p.split(u"=")
                    parameters[k] = v
                except:
                    pass
            contents, script_name = cls.format_script(parameters=parameters)
            script_file_path = os.path.join(output_dir_path, script_name)
            write_file(contents, script_file_path)
            if not quiet:
                print("Created file: %s" % script_file_path)



def main():
    Trainer().run()

if __name__ == "__main__":
    main()



