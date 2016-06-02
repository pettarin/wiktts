#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function
import io
import os

from ipapy.compatibility import to_unicode_string

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class SequenceLexiconEntry(object):
    """
    TBW
    """

    def __init__(self, word, phones):
        self.word = word
        self.phones = phones



def default_split(string):
    return string.split(u" ")



class SequenceLexicon(object):
    """
    TBW
    """

    def __init__(self):
        self.entries = []
        self.entries_dict = dict()

    def _update(self):
        self.entries_dict = dict()
        for e in self.entries:
            if not e.word in self.entries_dict:
                self.entries_dict[e.word] = []
            self.entries_dict[e.word].append(e)

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        for e in self.entries:
            yield e

    @property
    def words(self):
        return [e.word for e in self.entries]

    def entries_for_word(self, word):
        try:
            return self.entries_dict[word]
        except KeyError:
            return []

    def read_file(self, lexicon_file_path, field_to_sequence_function=default_split, comment=u"#", delimiter=u"\t", word_index=0, phones_index=1):
        if (lexicon_file_path is None) or (not os.path.isfile(lexicon_file_path)):
            raise ValueError("The lexicon file path must exist. (Got '%s')" % lexicon_file_path)
        comment = to_unicode_string(comment)
        delimiter = to_unicode_string(delimiter)
        with io.open(lexicon_file_path, "r", encoding="utf-8") as lexicon_file:
            for line in lexicon_file:
                line = line.strip()
                if not line.startswith(comment):
                    acc = line.split(delimiter)
                    self.entries.append(SequenceLexiconEntry(
                        word=acc[word_index],
                        phones=field_to_sequence_function(acc[phones_index])
                    ))
        self._update()



