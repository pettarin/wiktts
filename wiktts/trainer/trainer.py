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
from wiktts.trainer.g2ptool import FILTER_IPA_CHARS
from wiktts.trainer.g2ptool import G2P_TOOLS
from wiktts.trainer.g2ptool import G2PPhonetisaurus
from wiktts.trainer.g2ptool import G2PSequitur

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class Trainer(CommandLineTool):

    AP_DESCRIPTION = u"Prepare train/test/symbol files for LTS/G2P tools."
    AP_ARGUMENTS = [
        {
            "name": "g2ptool",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "G2P tool [%s]" % u"|".join(G2P_TOOLS)
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
            "default": u"cvsl",
            "help": "Include only the given IPA characters [%s] (default: 'cvsl')" % u"|".join(FILTER_IPA_CHARS)
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
            "name": "--train-size-perc",
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
    ]

    def actual_command(self):
        # get options
        g2ptool = self.vargs["g2ptool"]
        lexicon = self.vargs["lexicon"]
        output_dir_path =  self.vargs["outputdir"]
        quiet = self.vargs["quiet"]
        print_stats = self.vargs["stats"] 
        comment = self.vargs["comment"]
        delimiter = self.vargs["delimiter"]
        word_index = self.vargs["word_index"]
        ipa_index = self.vargs["ipa_index"]
        train_size = self.vargs["train_size_perc"] if self.vargs["train_size_int"] is None else self.vargs["train_size_int"]
        include_chars = self.vargs["include_chars"]

        # make sure
        if g2ptool not in [u"phonetisaurus", u"sequitur"]:
            self.error("The available G2P tools are: %s. (Got: '%s')" % (G2P_TOOLS, g2ptool))

        # make sure output directory exists
        if not os.path.isdir(output_dir_path):
            # TODO create dir instead?
            self.error("The output directory does not exist! (Got: '%s')" % output_dir_path)

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
        if g2ptool == u"phonetisaurus":
            cls = G2PPhonetisaurus
        else:
            cls = G2PSequitur
        g2ptool = cls(
            lexicon=lexi,
            include_chars=include_chars,
            mapper_name=None,
            train_size=train_size
        )

        # output to file
        base = os.path.join(output_dir_path, os.path.basename(lexicon))
       
        train_file_path = base + u".train"
        write_file(g2ptool.format_train(), train_file_path)
        
        test_file_path = base + u".test"
        write_file(g2ptool.format_test(), test_file_path)

        symb_file_path = base + u".symbols"
        write_file(g2ptool.format_symbol_set(), symb_file_path)

        # output as requested
        #if output_file_path is not None:
        #    write_file(formatted_data, output_file_path)
        if not quiet:
            print("Created file: %s" % train_file_path)
            print("Created file: %s" % test_file_path)
            print("Created file: %s" % symb_file_path)

        # print statistics if requested
        if print_stats:
            total = len(lexi)
            print("Words:")
            print("  Total: %d" % (g2ptool.train_size + g2ptool.test_size))
            print("  Train: %d" % g2ptool.train_size)
            print("  Test:  %d" % g2ptool.test_size)
            print("Symbols:")
            print("  Total: %d" % (g2ptool.symbol_set_size))
            print("  Train: %d" % (g2ptool.train_symbol_set_size))
            print("  Test:  %d" % (g2ptool.test_symbol_set_size))



def main():
    Trainer().run()

if __name__ == "__main__":
    main()



