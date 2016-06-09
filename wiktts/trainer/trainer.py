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
from wiktts.mappedpronunciationlexicon import MappedPronunciationLexicon
from wiktts.trainer.tool import TOOLS

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

MAPPERS = [
    u"arpabet",
    u"auto",
    u"kirshenbaum"
]

class Trainer(CommandLineTool):

    AP_PROGRAM = u"wiktts.trainer"
    AP_DESCRIPTION = u"Prepare train/test/symbol files for ML tools."
    AP_ARGUMENTS = [
        {
            "name": "tool",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "ML tool [%s]" % u"|".join(TOOLS.keys())
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
            "default": u"letters",
            "help": "Map only the specified IPA characters [%s] (default: 'letters')" % u"|".join(MappedPronunciationLexicon.FILTER_IPA_CHARS)
        },
        {
            "name": "--mapper",
            "nargs": "?",
            "type": str,
            "default": u"auto",
            "help": "Map IPA characters using the specified mapper [%s] (default: 'auto')" % u"|".join(MAPPERS)
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
            "name": "--stats",
            "action": "store_true",
            "help": "Print statistics"
        },
        {
            "name": "--script-only",
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
            "name": "--lowercase",
            "action": "store_true",
            "help": "Lowercase all the words"
        },
    ]

    def __init__(
            self,
            lexicon=None,
            tool=None,
            mapper=None,
            output_directory_path=None,
        ):
        super(Trainer, self).__init__()
        self.lexicon = lexicon
        self.tool = tool
        self.mapper = mapper
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

    def _create_lexicon(self, lexicon_file_path, comment, delimiter, word_index, pron_index, lowercase, chars):
        self.lexicon = MappedPronunciationLexicon(lowercase=lowercase)
        self.lexicon.read_file(
            lexicon_file_path=lexicon_file_path,
            comment=comment,
            delimiter=delimiter,
            indices=[word_index, pron_index]
        )
        self.lexicon.filter_chars(chars=chars)

    def _create_mapper(self, mapper_name):
        if mapper_name == u"kirshenbaum":
            from ipapy.kirshenbaummapper import KirshenbaumMapper
            mapper = KirshenbaumMapper()
        elif mapper_name == u"arpabet":
            from ipapy.arpabetmapper import ARPABETMapper
            mapper = ARPABETMapper()
        else:
            # create default mapper
            mapper = Mapper()
            # NOTE sorting by canonical representation ensures consistency of the symbol set
            #      across different tools (for the same input lexicon)
            phones = sorted([p.canonical_representation for p in self.lexicon.phones])
            for i, p in enumerate(phones):
                # NOTE the key is a 1-element tuple: (canonical_repr, )
                mapper[(p,)] = u"%03d" % (i + 1)
        self.mapper = mapper

    def output_script(self, base, parameters_string):
        parameters = {
            "output_dir_path": self.output_directory_path,
            "base": os.path.basename(base)
        }
        for p in parameters_string.split(u","):
            try:
                k, v = p.split(u"=")
                parameters[k] = v
            except:
                pass
        script_file_path = os.path.join(self.output_directory_path, self.tool.SCRIPT_FILE_NAME)
        contents = self.tool.format_script(parameters=parameters)
        write_file(contents, script_file_path)
        return [script_file_path]

    def output_ml_files(self, base):
        acc = []
        acc.append(base + u".train")
        write_file(self.tool.format_train(), acc[-1])
        acc.append(base + u".train.tab")
        write_file(self.tool.format_tab(train=True, test=False), acc[-1])
        acc.append(base + u".train.words")
        write_file(self.tool.format_words(train=True, test=False), acc[-1]) 
        acc.append(base + u".train.symbols")
        write_file(self.tool.format_symbols(train=True, test=False), acc[-1])
        acc.append(base + u".test")
        write_file(self.tool.format_test(), acc[-1])
        acc.append(base + u".test.tab")
        write_file(self.tool.format_tab(train=False, test=True), acc[-1])
        acc.append(base + u".test.words")
        write_file(self.tool.format_words(train=False, test=True), acc[-1]) 
        acc.append(base + u".test.symbols")
        write_file(self.tool.format_symbols(train=False, test=True), acc[-1])
        acc.append(base + u".tab")
        write_file(self.tool.format_tab(train=True, test=True, sort=True), acc[-1])
        acc.append(base + u".words")
        write_file(self.tool.format_words(train=True, test=True, sort=True), acc[-1]) 
        acc.append(base + u".symbols")
        write_file(self.tool.format_symbols(train=True, test=True), acc[-1])
        return acc

    def actual_command(self):
        # options to init the object
        self.output_directory_path =  self.vargs["outputdir"]
        lexicon_file_path = self.vargs["lexicon"]
        tool_name = self.vargs["tool"]
        mapper_name = self.vargs["mapper"]
        comment = self.vargs["comment"]
        delimiter = self.vargs["delimiter"]
        word_index = self.vargs["word_index"]
        pron_index = self.vargs["pron_index"]
        
        # options to filter/format results
        lowercase = self.vargs["lowercase"]
        chars = self.vargs["chars"]
        train_size = self.vargs["train_size_frac"] if self.vargs["train_size_int"] is None else self.vargs["train_size_int"]
        script_only = self.vargs["script_only"]
        script_parameters = self.vargs["script_parameters"]
       
        # options controlling print behavior
        print_stats = self.vargs["stats"] 
        created_files = []

        # checks
        if not os.path.isfile(lexicon_file_path):
            self.error(u"The lexicon file must exist. (Got '%s')" % lexicon_file_path)
        if tool_name not in TOOLS:
            self.error(u"The available tools are: %s. (Got: '%s')" % (TOOLS.keys(), tool_name))
        if mapper_name not in MAPPERS:
            self.error(u"The available mappers are: %s. (Got: '%s')" % (MAPPERS, mapper_name))
        self.tool = TOOLS[tool_name]
        base = os.path.join(self.output_directory_path, os.path.basename(lexicon_file_path))

        # output Bash script only?
        if script_only:
            created_files.extend(self.output_script(base, script_parameters))
            for f in created_files:
                self.print_stderr("Created file: %s" % f)
            return

        # load lexicon
        self._create_lexicon(lexicon_file_path, comment, delimiter, word_index, pron_index, lowercase, chars)
        # create and apply mapper
        self._create_mapper(mapper_name)
        self.lexicon.apply_mapper(mapper=self.mapper)
        # generate train/test sets
        self.lexicon.shuffle_and_partition(size=train_size, store=True)
        # create tool object
        self.tool = self.tool(
            lexicon=self.lexicon,
            mapper=self.mapper
        )
        
        # output ML files for tool
        created_files.extend(self.output_ml_files(base))
        
        # output stats
        stats = []
        stats.append(u"Lexicon path:          %s" % lexicon_file_path)
        stats.append(u"Output directory:      %s" % self.output_directory_path)
        stats.append(u"Lowercase words:       %s" % lowercase)
        stats.append(u"Map IPA characters:    %s" % chars)
        stats.append(u"Mapper:                %s" % mapper_name)
        stats.append(u"Tool:                  %s" % tool_name)
        stats.append(u"Train size:            %s" % str(train_size))
        stats.append(u"Words:")
        stats.append(u"  Total: %d" % len(self.lexicon))
        stats.append(u"  Train: %d" % len(self.lexicon.train_lexicon))
        stats.append(u"  Test:  %d" % len(self.lexicon.test_lexicon))
        stats.append(u"Symbols:")
        stats.append(u"  Total: %d" % len(self.lexicon.symbols))
        stats.append(u"  Train: %d" % len(self.lexicon.train_lexicon.symbols))
        stats.append(u"  Test:  %d" % len(self.lexicon.test_lexicon.symbols))
        created_files.append(base + u".trainer_stats")
        write_file(stats, created_files[-1])
        
        # output script
        created_files.extend(self.output_script(base, script_parameters))
        
        # print statistics if requested
        for f in created_files:
            self.print_stderr("Created file: %s" % f)
        if print_stats:
            self.print_stderr(u"\n".join(stats))



def main():
    Trainer().run()

if __name__ == "__main__":
    main()



