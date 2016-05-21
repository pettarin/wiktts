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
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

Data = namedtuple("Data", ["extracted", "id", "word", "ipa"]) 

ExtractionInfo = namedtuple("ExtractionInfo", ["mwdata", "pages_total", "pages_with_ipa"])

DEFAULT_FORMAT_BOTH = u"{EXTRACTED}\t{WORD}\t{IPA}"
DEFAULT_FORMAT_WITH = u"{WORD}\t{IPA}"
DEFAULT_FORMAT_WITHOUT = u"{ID}\t{WORD}"

PLACEHOLDERS = ["{ID}", "{WORD}", "{IPA}", "{EXTRACTED}", "{FILENAME}", "{FILEPATH}"]

def format_mwdata(data, template=None, dump_file_path=None, include_with=True, include_without=False):
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

    # select template
    if include_with and include_without:
        template = template or DEFAULT_FORMAT_BOTH
        filtered_data = data
    elif include_with:
        template = template or DEFAULT_FORMAT_WITH 
        filtered_data = [d for d in data if d.extracted]
    elif include_without:
        template = template or DEFAULT_FORMAT_WITHOUT
        filtered_data = [d for d in data if not d.extracted]
    else:
        template = template or DEFAULT_FORMAT_BOTH
        filtered_data = []

    # format data
    return [template.format(
        EXTRACTED=d.extracted,
        ID=d.id,
        WORD=d.word,
        IPA=d.ipa,
        FILENAME=relative_path,
        FILEPATH=absolute_path
    ) for d in filtered_data]



