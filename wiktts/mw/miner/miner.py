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
            "help": "MediaWiki dump file (.xml or .xml.bz2) or directory"
        },
        {
            "name": "--from-dir",
            "action": "store_true",
            "help": "Load .xml files inside this dump directory"
        },
        {
            "name": "--output-file",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Write output to file"
        },
        {
            "name": "--pages-per-chunk",
            "nargs": "?",
            "type": int,
            "default": 1000,
            "help": "Number of pages per output file (default: 1000)"
        },
        {
            "name": "--ns",
            "nargs": "+",
            "type": int,
            "default": [0],
            "help": "Extract only pages with the specified ns values (default: [0])"
        },
        {
            "name": "--hide-progress",
            "action": "store_true",
            "help": "Do not print extraction progress messages"
        },
        {
            "name": "--quiet",
            "action": "store_true",
            "help": "Do not print extraction results to stdout"
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
            "name": "--stats",
            "action": "store_true",
            "help": "Print statistics"
        },
        {
            "name": "--format",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Format output according to this template (available placeholders: %s)" % ", ".join(PLACEHOLDERS)
        },
    ]

    def actual_command(self):

        def process_chunk(pages, status):
            status.update(ipaext.extract_from_pages(pages))
            if show_progress:
                print(status.pretty_print(single_line=True))

        # get options
        ipa_parser = self.vargs["ipaparser"]
        dump_path = self.vargs["dump"]
        from_dir = self.vargs["from_dir"]
        output_file_path = self.vargs["output_file"]
        pages_per_chunk = self.vargs["pages_per_chunk"]
        ns = self.vargs["ns"]
        show_progress = not self.vargs["hide_progress"]
        quiet = self.vargs["quiet"]
        print_stats = self.vargs["stats"] 
        sort_results = not self.vargs["no_sort"]
        template = self.vargs["format"]
        all_pages = self.vargs["all"]
        all_with_lang = self.vargs["all_with_lang"]
        without_ipa = self.vargs["without_ipa"]

        # extract IPA strings
        status = MinerStatus()
        ipaext = IPAExtractor(ipa_parser_name=ipa_parser)
        mwp = Parser(full_parsing=False)
        if from_dir:
            # read all XML files from the dump directory
            for root, dirs, files in os.walk(dump_path):
                for f in [f for f in sorted(files) if f.endswith(".xml")]:
                    mwp.parse_file(os.path.join(root, f), append=False)
                    process_chunk(mwp.pages, status)
        else:
            # read from dump file, in chunks
            mws = Splitter(dump_file_path=dump_path, pages_per_chunk=pages_per_chunk, ns=ns)
            for mwchunk in mws.mwchunks:
                mwp.parse_string(mwchunk.contents, append=False)
                process_chunk(mwp.pages, status)
       
        # format data if file or stdout output should be produced
        if (output_file_path is not None) or (not quiet):
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
                dump_file_path=dump_path,
                include=include
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
            print(status.pretty_print(single_line=False))



def main():
    Miner().run()

if __name__ == "__main__":
    main()



