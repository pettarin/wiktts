#!/usr/bin/env python
# coding=utf-8

"""
Split a Wiktionary dump file.

It can output to files on disk or return an iterator over chunks in memory.

Each file or chunk can contain one or more MediaWiki pages.
"""

from __future__ import absolute_import
from __future__ import print_function
from collections import namedtuple
import bz2
import io
import os
import re
import tempfile

from wiktts.commandlinetool import CommandLineTool

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

Chunk = namedtuple("Chunk", ["pages_total", "pages_ns", "index", "contents"])

class Splitter(CommandLineTool):
    
    MEDIAWIKI_OPEN = u'<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10">\n'
    MEDIAWIKI_CLOSE = u'</mediawiki>'
    NS_REGEX = re.compile(r"<ns>([0-9]+)<\/ns>")

    AP_PROGRAM = u"wiktts.mw.splitter"
    AP_DESCRIPTION = u"Split a MediaWiki dump into multiple files"
    AP_ARGUMENTS = [
        {
            "name": "dumpfile",
            "nargs": None,
            "type": str,
            "default": None,
            "help": "Input MediaWiki dump.xml or dump.xml.bz2"
        },
        {
            "name": "--output-dir",
            "nargs": "?",
            "type": str,
            "default": None,
            "help": "Output files in this directory"
        },
        {
            "name": "--namespaces",
            "nargs": "+",
            "type": int,
            "default": [],
            "help": "Extract only pages with namespace in the specified list (default: all)"
        },
        {
            "name": "--pages-per-chunk",
            "nargs": "?",
            "type": int,
            "default": 1000,
            "help": "Number of pages per output file (default: 1000)"
        },
        {
            "name": "--prefix",
            "nargs": "?",
            "type": str,
            "default": "",
            "help": "Use this prefix for the output file names (default: '')"
        },
        {
            "name": "--max-number-pages",
            "nargs": "?",
            "type": int,
            "default": None,
            "help": "Number of pages to extract (default: all)"
        },
        {
            "name": "--head",
            "action": "store_true",
            "help": "Shortcut for --namespaces 0 --max-number-pages 1000"
        },
        {
            "name": "--count",
            "action": "store_true",
            "help": "Only count the number of pages"
        },
        {
            "name": "--hide-progress",
            "action": "store_true",
            "help": "Do not print extraction progress messages"
        },
        {
            "name": "--stats",
            "action": "store_true",
            "help": "Print statistics"
        },
    ]

    def __init__(
            self,
            dump_file_path=None,
            output_directory_path=None,
            output_file_prefix=u"",
            pages_per_chunk=1000,
            namespaces=[],
            max_number_pages=None
        ):
        super(Splitter, self).__init__()
        self.dump_file_path = dump_file_path
        self.output_directory_path = output_directory_path
        self.output_file_prefix = output_file_prefix
        self.pages_per_chunk = pages_per_chunk
        self.namespaces = namespaces
        self.max_number_pages = max_number_pages

    @property
    def dump_file_path(self):
        return self.__dump_file_path
    @dump_file_path.setter
    def dump_file_path(self, value):
        if value is not None:
            if not os.path.isfile(value):
                self.error(u"The dump file must exist. (Got '%s')" % value)
            if not (value.endswith(u".xml") or value.endswith(u".xml.bz2")):
                self.error(u"The dump file path must end in '.xml' (uncompressed) or '.xml.bz2' (compressed). (Got '%s')" % value)
        self.__dump_file_path = value

    @property
    def output_directory_path(self):
        return self.__output_directory_path
    @output_directory_path.setter
    def output_directory_path(self, value):
        if value is not None:
            if not os.path.isdir(value):
                self.error(u"The output directory must exist. (Got: '%s')" % value)
        self.__output_directory_path = value

    @property
    def pages_per_chunk(self):
        return self.__pages_per_chunk
    @pages_per_chunk.setter
    def pages_per_chunk(self, value):
        if value < 1:
            self.error(u"The number of pages per chunk must at least 1. (Got: '%d')" % value)
        self.__pages_per_chunk = value

    @property
    def namespaces(self):
        return self.__namespaces
    @namespaces.setter
    def namespaces(self, value):
        self.__namespaces = set(value)

    def actual_command(self):
        # options to init the object
        self.dump_file_path = self.vargs["dumpfile"]
        self.output_directory_path = self.vargs["output_dir"]
        self.pages_per_chunk = self.vargs["pages_per_chunk"]
        self.output_file_prefix = self.vargs["prefix"]
        self.namespaces = self.vargs["namespaces"]
        self.max_number_pages = self.vargs["max_number_pages"]
        
        # options to filter/count pages
        head = self.vargs["head"]
        count_pages = self.vargs["count"]

        # options controlling print behavior
        show_progress = not self.vargs["hide_progress"]
        print_stats = self.vargs["stats"]

        if head:
            self.namespaces = [0]
            self.max_number_pages = 1000
            self.print_stderr(u"Option --head: extracting first 1000 pages with namespaces 0")
        if count_pages:
            self.print_stderr(u"Pages total: %s" % self.count_pages())
        else:
            pages_total, pages_ns, files_created = self.split(show_progress=show_progress)
            if print_stats:
                self.print_stderr(u"Pages total:    %s" % pages_total)
                if len(self.namespaces) > 0:
                    self.print_stderr(u"Pages filtered: %s" % pages_ns)
                self.print_stderr(u"Files created:  %s" % files_created)

    def open(self):
        """
        Open the dump file, either compressed or uncompressed,
        returning a file-like object.
        """
        if self.dump_file_path is None:
            raise ValueError(u"The dump file path has not been set yet")
        if self.dump_file_path.endswith(u".xml.bz2"):
            return bz2.BZ2File(self.dump_file_path, "r")
        return io.open(self.dump_file_path, "rb")

    def count_pages(self):
        """
        Shortcut to count the number of pages without full parsing.
        """
        with self.open() as dump_file_obj:
            pages_total = 0
            for line in dump_file_obj:
                # NOTE: it is "<page>" and not u"<page>"
                #       because bz2.BZ2File returns byte strings
                if line.strip() == "<page>":
                    pages_total += 1
        return pages_total

    def split(self, show_progress=False):
        """
        Split the dump into chunks.
        """
        if self.output_directory_path is None:
            self.output_directory_path = tempfile.mkdtemp()
        output_file_name_template = os.path.join(self.output_directory_path, self.output_file_prefix + u"%09d.xml")
        pages_total = 0
        pages_ns = 0
        current_chunk_index = 0
        for mwchunk in self.mwchunks:
            file_path = output_file_name_template % (mwchunk.index)
            with io.open(file_path, "w", encoding="utf-8") as chunk_file:
                chunk_file.write(mwchunk.contents)
            if show_progress:
                self.print_stderr(file_path)
        return (mwchunk.pages_total, mwchunk.pages_ns, mwchunk.index)

    @property
    def mwchunks(self):
        """
        A generator to loop through the MWChunk objects in the dump.
        """
        pages_total = 0
        pages_ns = 0
        in_page = False
        current_page_lines = []
        current_page_has_ns = None
        current_chunk_lines = []
        current_chunk_index = 0
        pages_in_current_chunk = 0
        with self.open() as dump_file_obj:
            for line in dump_file_obj:
                # convert bytes to Unicode object via UTF-8
                line = line.decode("utf-8")
                line_stripped = line.strip()
                if in_page:
                    # inside <page>
                    if current_page_has_ns is None:
                        # we haven't find <ns>...</ns> yet, so check the current line
                        m = re.match(self.NS_REGEX, line.strip())
                        if m is not None:
                            # the current line is the <ns>...</ns> line, set the current_page_has_ns flag
                            try:
                                current_page_has_ns = int(m.group(1)) in self.namespaces
                            except:
                                pass
                    # append contents to tmp buffer
                    current_page_lines.append(line)
                    if line_stripped == "</page>":
                        # we are done with this page
                        if current_page_has_ns:
                            # add current page to current chunk
                            current_chunk_lines.extend(current_page_lines)
                            pages_in_current_chunk += 1
                            pages_ns += 1
                            if (self.max_number_pages is not None) and (pages_ns == self.max_number_pages):
                                # output chunk and exit
                                current_chunk_index += 1
                                current_chunk_contents = self.MEDIAWIKI_OPEN + u"".join(current_chunk_lines) + self.MEDIAWIKI_CLOSE
                                yield Chunk(pages_total, pages_ns, current_chunk_index, current_chunk_contents)
                                return
                            if pages_in_current_chunk == self.pages_per_chunk:
                                # output chunk 
                                current_chunk_index += 1
                                current_chunk_contents = self.MEDIAWIKI_OPEN + u"".join(current_chunk_lines) + self.MEDIAWIKI_CLOSE
                                yield Chunk(pages_total, pages_ns, current_chunk_index, current_chunk_contents)
                                pages_in_current_chunk = 0
                                current_chunk_lines = []
                                current_page_lines = []
                        #else:
                        #    # do not add page, it does not have the right ns
                        #    pass
                        in_page = False
                else:
                    # waiting for the next <page>
                    if line_stripped == "<page>":
                        # open a new page
                        in_page = True
                        pages_total += 1
                        current_page_lines = [line]
                        if len(self.namespaces) == 0:
                            # no namespaces => output them all
                            current_page_has_ns = True
                        else:
                            # namespaces => set to None, so that we will match the page ns against the wanted ones
                            current_page_has_ns = None
            if pages_in_current_chunk > 0:
                # output last chunk, if any
                current_chunk_index += 1
                current_chunk_contents = self.MEDIAWIKI_OPEN + u"".join(current_chunk_lines) + self.MEDIAWIKI_CLOSE
                yield Chunk(pages_total, pages_ns, current_chunk_index, current_chunk_contents)



def main():
    Splitter().run()

if __name__ == "__main__":
    main()



