#!/usr/bin/env python
# coding=utf-8

"""
Extract IPA strings from a given MediaWiki dump file or directory.
"""

from __future__ import absolute_import
from __future__ import division 
from __future__ import print_function
import os

from wiktts import write_file
from wiktts.commandlinetool import CommandLineTool
from wiktts.mw.data import PLACEHOLDERS, format_mwdata
from wiktts.mw.miner.ipaextractor import IPAExtractor
from wiktts.mw.miner.minerstatus import MinerStatus
from wiktts.mw.parser import Parser
from wiktts.mw.splitter.splitter import Splitter

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class Miner(CommandLineTool):

    AP_PROGRAM = u"wiktts.mw.miner"
    AP_DESCRIPTION = u"Extract IPA strings from a given MediaWiki dump file."
    AP_ARGUMENTS = [
        {
            "name": "ipaparser",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "IPA parser (built-in name or file path)"
        },
        {
            "name": "dump",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "MediaWiki dump.xml or dump.xml.bz2 or dump/"
        },
        {
            "name": "outputdir",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "Output files in this directory"
        },
        {
            "name": "--pages-per-chunk",
            "nargs": "?",
            "type": int,
            "default": 1000,
            "help": "Number of pages per output file (default: 1000)"
        },
        {
            "name": "--namespaces",
            "nargs": "+",
            "type": int,
            "default": [0],
            "help": "Extract only pages with namespace in the specified list (default: [0])"
        },
        {
            "name": "--all",
            "action": "store_true",
            "help": "Print extraction results for all pages (with/without correct language block)"
        },
        {
            "name": "--all-with-lang",
            "action": "store_true",
            "help": "Print extraction results for all pages with correct language block (with/without IPA string)"
        },
        {
            "name": "--without-ipa",
            "action": "store_true",
            "help": "Print extraction results only for pages with correct language block but without IPA string"
        },
        {
            "name": "--no-sort",
            "action": "store_true",
            "help": "Do not sort the extraction results"
        },
        {
            "name": "--hide-progress",
            "action": "store_true",
            "help": "Do not print extraction progress messages"
        },
        {
            "name": "--stats",
            "action": "store_true",
            "help": "Print statistics to standard output"
        },
        {
            "name": "--stdout",
            "action": "store_true",
            "help": "Print extraction results to standard output"
        },
        {
            "name": "--format",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Format output according to this template (available placeholders: %s)" % ", ".join(PLACEHOLDERS)
        },
    ]

    def __init__(
            self,
            ipa_parser=None,
            dump_path=None,
            output_directory_path=None,
            pages_per_chunk=1000,
            namespaces=[0]
        ):
        super(Miner, self).__init__()
        self.__dump_path_is_file = None
        self.ipa_parser = ipa_parser
        self.dump_path = dump_path
        self.output_directory_path = output_directory_path
        self.pages_per_chunk = pages_per_chunk
        self.namespaces = namespaces

    @property
    def dump_path(self):
        return self.__dump_path
    @dump_path.setter
    def dump_path(self, value):
        if value is not None:
            if not (os.path.isfile(value) or os.path.isdir(value)):
                self.error("The dump file or directory must exist. (Got '%s')" % value)
            if os.path.isfile(value):
                if not (value.endswith(".xml") or value.endswith(".xml.bz2")):
                    self.error("The dump file path must end in '.xml' (uncompressed) or '.xml.bz2' (compressed). (Got '%s')" % value)
                self.__dump_path_is_file = True 
            else:
                self.__dump_path_is_file = False
        self.__dump_path = value

    @property
    def dump_path_is_file(self):
        return self.__dump_path_is_file

    @property
    def output_directory_path(self):
        return self.__output_directory_path
    @output_directory_path.setter
    def output_directory_path(self, value):
        if value is not None:
            if not os.path.isdir(value):
                self.error("The output directory must exist. (Got: '%s')" % value)
        self.__output_directory_path = value

    @property
    def pages_per_chunk(self):
        return self.__pages_per_chunk
    @pages_per_chunk.setter
    def pages_per_chunk(self, value):
        if value < 1:
            self.error("The number of pages per chunk must at least 1. (Got: '%d')" % value)
        self.__pages_per_chunk = value

    @property
    def namespaces(self):
        return self.__namespaces
    @namespaces.setter
    def namespaces(self, value):
        self.__namespaces = set(value)

    def extract_ipa_strings(self, show_progress=False):
        """
        Extract IPA strings from the given dump.

        Return a MinerStatus object.
        """
        def process_chunk(pages, status):
            """
            Process a chunk, that is, a set of pages,
            updating the status object.
            """
            status.update(ipaext.extract_from_pages(pages))
            if show_progress:
                self.print_stderr(status.pretty_print(single_line=True))
        # status object to be returned
        status = MinerStatus()
        ipaext = IPAExtractor(ipa_parser_name=self.ipa_parser)
        mwp = Parser(full_parsing=False)
        if self.dump_path_is_file:
            # read from dump file, in chunks
            mws = Splitter(dump_file_path=self.dump_path, pages_per_chunk=self.pages_per_chunk, namespaces=self.namespaces)
            for mwchunk in mws.mwchunks:
                mwp.parse_string(mwchunk.contents, append=False)
                process_chunk(mwp.pages, status)
        else:
            # read all XML files from the dump directory
            for root, dirs, files in os.walk(self.dump_path):
                for f in [f for f in sorted(files) if f.endswith(".xml")]:
                    mwp.parse_file(os.path.join(root, f), append=False)
                    process_chunk(mwp.pages, status)
        return status

    def actual_command(self):
        # options to init the object
        self.ipa_parser = self.vargs["ipaparser"]
        self.dump_path = self.vargs["dump"]
        self.output_directory_path = self.vargs["outputdir"]
        self.pages_per_chunk = self.vargs["pages_per_chunk"]
        self.namespaces = self.vargs["namespaces"]

        # options to filter/format results
        all_pages = self.vargs["all"]
        all_with_lang = self.vargs["all_with_lang"]
        without_ipa = self.vargs["without_ipa"]
        template = self.vargs["format"]
        sort_results = not self.vargs["no_sort"]

        # options controlling print behavior
        show_progress = not self.vargs["hide_progress"]
        print_stats = self.vargs["stats"] 
        print_stdout = self.vargs["stdout"] 

        # extract IPA strings
        status = self.extract_ipa_strings(show_progress=show_progress)

        # select the data to include in the output
        if all_pages:
            include = (True, True, True, True)
        elif all_with_lang:
            include = (True, False, True, True)
        elif without_ipa:
            include = (True, False, False, True)
        else:
            include = (True, False, True, False)
        # format data
        formatted_data = format_mwdata(
            status.mwdata,
            template=template,
            dump_file_path=self.dump_path,
            include=include
        )
        # sort if requested
        if sort_results:
            formatted_data = sorted(formatted_data)
        
        # output files 
        output_file_path = os.path.join(self.output_directory_path, os.path.basename(self.dump_path) + u".lex")
        write_file(formatted_data, output_file_path)
        stats_file_path = os.path.join(self.output_directory_path, os.path.basename(self.dump_path) + u".miner_stats")
        stats = []
        stats.append(u"IPA parser:       %s" % self.ipa_parser)
        stats.append(u"Dump path:        %s" % self.dump_path)
        stats.append(u"Output directory: %s" % self.output_directory_path)
        stats.append(u"Pages per chunk:  %d" % self.pages_per_chunk)
        stats.append(u"Namespaces:       %s" % self.namespaces)
        stats.append(status.pretty_print(single_line=False))
        write_file(stats, stats_file_path)

        # print to stdout if requested 
        if print_stdout:
            for d in formatted_data:
                self.print_stdout(d)

        # print statistics if requested
        self.print_stderr(u"Created file %s" % output_file_path)
        self.print_stderr(u"Created file %s" % stats_file_path)
        if print_stats:
            self.print_stderr(u"\n".join(stats))



def main():
    Miner().run()

if __name__ == "__main__":
    main()



