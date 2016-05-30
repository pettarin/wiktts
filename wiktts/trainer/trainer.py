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
from ipapy.mapper import Mapper

from wiktts import write_file
from wiktts.commandlinetool import CommandLineTool
from wiktts.lexicon import FILTER_IPA_CHARS
from wiktts.lexicon import PLACEHOLDERS
from wiktts.lexicon import MappableLexicon
from wiktts.trainer.tool import TOOLS
from wiktts.trainer.tool import ToolPhonetisaurus08a
from wiktts.trainer.tool import ToolPhonetisaurusMaster
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
            "help": "Clean lexicon input file"
        },
        {
            "name": "outputdir",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "Write output files to this directory"
        },
        {
            "name": "--chars",
            "nargs": "?",
            "type": str,
            "default": u"cv",
            "help": "Output the IPA characters of specified type [%s] (default: 'cv')" % u"|".join(FILTER_IPA_CHARS)
        },
        {
            "name": "--mapper",
            "nargs": "?",
            "type": str,
            "default": u"auto",
            "help": "Map IPA chars using the specified mapper [arpabet|auto|kirshenbaum] (default: 'auto')"
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
            "name": "--script-parameters",
            "nargs": "?",
            "type": str,
            "default": u"",
            "help": "Parameters to configure the Bash script to run the ML tool"
        },
        {
            "name": "--create-output-dir",
            "action": "store_true",
            "help": "Create the output directory if it does not exist"
        },
    ]

    def actual_command(self):
        # get options
        tool_name = self.vargs["tool"]
        lexicon_file_path = self.vargs["lexicon"]
        output_dir_path =  self.vargs["outputdir"]
        chars = self.vargs["chars"]
        quiet = self.vargs["quiet"]
        print_stats = self.vargs["stats"] 
        comment = self.vargs["comment"]
        delimiter = self.vargs["delimiter"]
        word_index = self.vargs["word_index"]
        ipa_index = self.vargs["ipa_index"]
        train_size = self.vargs["train_size_frac"] if self.vargs["train_size_int"] is None else self.vargs["train_size_int"]
        output_script_only = self.vargs["output_script_only"]
        script_parameters = self.vargs["script_parameters"]
        create_output_dir = self.vargs["create_output_dir"]
        mapper_name = self.vargs["mapper"]

        # make sure
        if tool_name not in TOOLS:
            self.error("The available tools are: %s. (Got: '%s')" % (TOOLS, tool_name))

        # make sure output directory exists
        if not os.path.isdir(output_dir_path):
            if create_output_dir:
                os.makedirs(output_dir_path)
            else:
                self.error("The output directory does not exist! (Got: '%s') Use '--create-output-dir' to create it. " % output_dir_path)

        # output file names
        base = os.path.join(output_dir_path, os.path.basename(lexicon_file_path))
        train_file_path = base + u".train"
        test_file_path = base + u".test"
        symb_file_path = base + u".symbols"
        script_file_path = None
        if tool_name == u"phonetisaurus_08a":
            cls = ToolPhonetisaurus08a
        elif tool_name == u"phonetisaurus_master":
            cls = ToolPhonetisaurusMaster
        else:
            cls = ToolSequitur

        if not output_script_only:
            # read lexicon with cleaned IPA strings
            #print("Building Lexicon...")
            lexicon = MappableLexicon()
            lexicon.read_file(
                lexicon_file_path=lexicon_file_path,
                comment=comment,
                delimiter=delimiter,
                word_index=word_index,
                ipa_index=ipa_index
            )
            #print("Filtering...")
            lexicon.filter_ipa_chars(chars)
            
            # create and apply mapper
            #print("Creating mapping...")
            if mapper_name == u"kirshenbaum":
                from ipapy.kirshenbaummapper import KirshenbaumMapper
                mapper = KirshenbaumMapper()
            elif mapper_name == u"arpabet":
                from ipapy.arpabetmapper import ARPABETMapper
                mapper = ARPABETMapper()
            else:
                mapper = Mapper()
                i = 1
                for p in lexicon.phones:
                    mapper[(p.canonical_representation,)] = u"%03d" % i
                    i += 1
            #print("Mapping...")
            lexicon.apply_mapper(mapper)
            
            # generate train/test/symbol sets
            #print("Sets...")
            lexicon.generate_sets(train_size=train_size)
            
            # create training, test, and symbol sets
            #print("Outputting...")
            tool_formatter = cls(
                lexicon=lexicon,
                mapper=mapper
            )
            write_file(tool_formatter.format_train(), train_file_path)
            write_file(tool_formatter.format_test(), test_file_path)
            write_file(tool_formatter.format_symbol_set(), symb_file_path)
            # print statistics if requested
            if print_stats:
                total = len(lexicon)
                print("Words:")
                print("  Total: %d" % (lexicon.train_size + lexicon.test_size))
                print("  Train: %d" % lexicon.train_size)
                print("  Test:  %d" % lexicon.test_size)
                print("Symbols:")
                print("  Total: %d" % (lexicon.symbol_set_size))
                print("  Train: %d" % (lexicon.train_symbol_set_size))
                print("  Test:  %d" % (lexicon.test_symbol_set_size))
            if not quiet:
                print("Created file: %s" % train_file_path)
                print("Created file: %s" % test_file_path)
                print("Created file: %s" % symb_file_path)

        # output script
        parameters = {"output_dir_path": output_dir_path, "base": os.path.basename(base)}
        for p in script_parameters.split(u","):
            try:
                k, v = p.split(u"=")
                key = u"%s_%s" % (tool, k)
                parameters[key] = v
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



