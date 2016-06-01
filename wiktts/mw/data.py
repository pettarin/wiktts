#!/usr/bin/env python
# coding=utf-8

"""
Representation of an IPA extraction result as a named tuple,
and related useful functions.
"""

from __future__ import absolute_import
from __future__ import print_function
from collections import namedtuple
import io
import os

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

Data = namedtuple("Data", ["haslanguageblock", "extracted", "id", "word", "ipa"]) 

ExtractionInfo = namedtuple("ExtractionInfo", ["mwdata", "pages_total", "pages_with_language_block", "pages_with_ipa"])

DEFAULT_FORMAT_LANG_EXTRACTED = u"{WORD}\t{IPA}"
DEFAULT_FORMAT_LANG_NOTEXTRACTED = u"{ID}\t{WORD}"
DEFAULT_FORMAT_LANG_BOTH = u"{EXTRACTED}\t{ID}\t{WORD}\t{IPA}"
DEFAULT_FORMAT_NOTLANG = u"{ID}\t{WORD}"

DEFAULT_FORMAT_ANY = u"{HASLANGUAGEBLOCK}\t{EXTRACTED}\t{ID}\t{WORD}\t{IPA}"

DEFAULT_FORMAT = {
    (False, False, False, False): DEFAULT_FORMAT_ANY,
    (False, False, False, True): DEFAULT_FORMAT_ANY,
    (False, False, True, False): DEFAULT_FORMAT_ANY,
    (False, False, True, True): DEFAULT_FORMAT_ANY,

    (False, True, False, False): DEFAULT_FORMAT_NOTLANG,
    (False, True, False, True): DEFAULT_FORMAT_NOTLANG,
    (False, True, True, False): DEFAULT_FORMAT_NOTLANG,
    (False, True, True, True): DEFAULT_FORMAT_NOTLANG,

    (True, False, False, False): DEFAULT_FORMAT_ANY,
    (True, False, False, True): DEFAULT_FORMAT_LANG_NOTEXTRACTED,
    (True, False, True, False): DEFAULT_FORMAT_LANG_EXTRACTED,
    (True, False, True, True): DEFAULT_FORMAT_LANG_BOTH,

    (True, True, False, False): DEFAULT_FORMAT_ANY,
    (True, True, False, True): DEFAULT_FORMAT_ANY,
    (True, True, True, False): DEFAULT_FORMAT_ANY,
    (True, True, True, True): DEFAULT_FORMAT_ANY,
}

PLACEHOLDERS = ["{ID}", "{WORD}", "{IPA}", "{EXTRACTED}", "{HASLANGUAGEBLOCK}", "{FILENAME}", "{FILEPATH}"]

def format_mwdata(data, template=None, dump_file_path=None, include=(True, False, True, False)):
    # include = (haslanguageblock, NOT haslanguageblock, extracted, NOT extracted)

    # make sure strings are Unicode objects
    try:
        # python 2
        template = template.decode("utf-8")
        dump_file_path = dump_file_path.decode("utf-8")
    except:
        # python 3
        pass
    absolute_path = os.path.abspath(dump_file_path) if dump_file_path is not None else ""
    relative_path = os.path.basename(dump_file_path) if dump_file_path is not None else ""

    # filter data: haslanguageblock
    if include[0] and include[1]:
        filtered_data = data
    elif include[0]:
        filtered_data = [d for d in data if d.haslanguageblock]
    elif include[1]:
        filtered_data = [d for d in data if not d.haslanguageblock]
    else:
        filtered_data = []
    # filter data: extracted
    if include[2] and include[3]:
        #filtered_data = filtered_data
        pass 
    elif include[2]:
        filtered_data = [d for d in filtered_data if d.extracted]
    elif include[3]:
        filtered_data = [d for d in filtered_data if not d.extracted]
    else:
        filtered_data = []
    # select template
    template = template or DEFAULT_FORMAT[include]

    # format data
    return [template.format(
        EXTRACTED=d.extracted,
        HASLANGUAGEBLOCK=d.haslanguageblock,
        ID=d.id,
        WORD=d.word,
        IPA=d.ipa,
        FILENAME=relative_path,
        FILEPATH=absolute_path
    ) for d in filtered_data]



