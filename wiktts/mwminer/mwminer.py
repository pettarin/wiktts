#!/usr/bin/env python
# coding=utf-8

"""
Extract IPA strings from a given MediaWiki dump file or directory.
"""

from __future__ import absolute_import
from __future__ import division 
from __future__ import print_function
import os

from wiktts.commandlinetool import CommandLineTool
from wiktts.mwminer.mwdata import PLACEHOLDERS, MWData, format_mwdata, write_mwdata
from wiktts.mwminer.mwsplitter import MWSplitter
from wiktts.mwminer.mwparser import MWParser
from wiktts.mwminer.mwipaextractor import MWIPAExtractor
from wiktts.mwminer.mwminerstatus import MWMinerStatus

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class MWMiner(CommandLineTool):

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
            "help": "Load .xml files inside dump directory"
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
            "help": "Print extraction results for all pages (with and without IPA string)"
        },
        {
            "name": "--without",
            "action": "store_true",
            "help": "Print extraction results only for pages without IPA string"
        },
        {
            "name": "--sort",
            "action": "store_true",
            "help": "Sort the extraction results"
        },
        {
            "name": "--stats",
            "action": "store_true",
            "help": "Print the count of all pages and pages with IPA string"
        },
        {
            "name": "--format",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Format output according to this string (available placeholders: %s)" % ", ".join(PLACEHOLDERS)
        },
        {
            "name": "--tsv",
            "action": "store_true",
            "help": "Shortcut --format \"{WORD}\\t{IPA}\""
        },
        {
            "name": "--canonical",
            "action": "store_true",
            "help": "Shortcut --ns 0 --tsv --sort"
        },
    ]

    def actual_command(self):

        def process_chunk(pages, status):
            status.update(ipaext.extract_from_pages(pages))
            if show_progress:
                print("Pages Total/With IPA: %d / %d (%s)" % (status.pages_total, status.pages_with_ipa, status.percentage))

        # get options
        ipa_parser = self.vargs["ipaparser"]
        dump_path = self.vargs["dump"]
        from_dir = self.vargs["from_dir"]
        output_file_path = self.vargs["output_file"]
        pages_per_chunk = self.vargs["pages_per_chunk"]
        ns = self.vargs["ns"]
        show_progress = not self.vargs["hide_progress"]
        quiet = self.vargs["quiet"]
        if self.vargs["all"]:
            include_with = True
            include_without = True
        elif self.vargs["without"]:
            include_with = False
            include_without = True
        else:
            include_with = True
            include_without = False
        print_stats = self.vargs["stats"] 
        sort_results = self.vargs["sort"]
        template = self.vargs["format"]
        if self.vargs["tsv"]:
            template = "{WORD}\t{IPA}"
        if self.vargs["canonical"]:
            ns = [0]
            template = "{WORD}\t{IPA}"
            sort_results = True

        # extract IPA strings
        status = MWMinerStatus()
        ipaext = MWIPAExtractor(ipa_parser_name=ipa_parser)
        mwp = MWParser(full_parsing=False)
        if from_dir:
            # read all XML files from the dump directory
            for root, dirs, files in os.walk(dump_path):
                for f in [f for f in sorted(files) if f.endswith(".xml")]:
                    mwp.parse_file(os.path.join(root, f), append=False)
                    process_chunk(mwp.pages, status)
        else:
            # read from dump file, in chunks
            mws = MWSplitter(dump_file_path=dump_path, pages_per_chunk=pages_per_chunk, ns=ns)
            for mwchunk in mws.mwchunks:
                mwp.parse_string(mwchunk.contents, append=False)
                process_chunk(mwp.pages, status)
       
        # format data
        formatted_data = format_mwdata(
            status.mwdata,
            template=template,
            dump_file_path=dump_path,
            include_with=include_with,
            include_without=include_without
        )
        if sort_results:
            formatted_data = sorted(formatted_data)

        # output as requested
        if output_file_path is not None:
            write_mwdata(formatted_data, output_file_path)
        if not quiet:
            for d in formatted_data:
                print(d)
        if print_stats:
            print("Pages Total:    %d" % status.pages_total)
            print("Pages With IPA: %d (%s)" % (status.pages_with_ipa, status.percentage))



def main():
    MWMiner().run()

if __name__ == "__main__":
    main()



