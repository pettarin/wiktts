#!/usr/bin/env python
# coding=utf-8

"""
TBW
"""

from __future__ import absolute_import
from __future__ import print_function
from collections import MutableSequence
import io
import os
import random

from ipapy.compatibility import to_str
from ipapy.compatibility import to_unicode_string

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2016, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__email__ = "alberto@albertopettarin.it"

class LexiconEntry(object):
    """
    TBW
    """

    def __init__(self, raw_values, lowercase=False):
        self.key = None
        self.value = None
        self.valid = False
        self._set_key(raw_values=raw_values, lowercase=lowercase)
        self._set_value(raw_values=raw_values, lowercase=lowercase)

    def _set_key(self, raw_values, lowercase):
        if len(raw_values) >= 1:
            self.key = raw_values[0]
            if lowercase:
                self.key = self.key.lower()

    def _set_value(self, raw_values, lowercase):
        if len(raw_values) >= 2:
            self.valid = True
            self.value = raw_values[1]



class Lexicon(MutableSequence):
    """
    TBW
    """

    ENTRY_TYPE = LexiconEntry

    def __init__(self, entries=None, lowercase=False):
        self.__ordered_dict = None
        self.entries = [] if entries is None else entries
        self.lowercase = lowercase
        self.train_lexicon = None
        self.test_lexicon = None
        self._update_ordered_dict()

    def _update_ordered_dict(self):
        self.__ordered_dict = dict()
        for i, e in enumerate(self.entries):
            self._add_entry_to_ordered_dict(i, e)

    def _add_entry_to_ordered_dict(self, i, e):
        k = e.key
        try:
            self.__ordered_dict[k].append(i)
        except KeyError:
            self.__ordered_dict[k] = [i]

    def _remove_entry_from_ordered_dict(self, i):
        k = self[i].key
        l = self.__ordered_dict[k]
        del l[l.index(k)]
        if len(l) == 0:
            del self.__ordered_dict[k]

    def __str__(self):
        return to_str(u"".join([e.__str__() for e in self.entries]))

    def __unicode__(self):
        return u"".join([e.__unicode__() for e in self.entries])

    def __repr__(self):
        return u"\n".join([e.__repr__() for e in self.entries])

    def __iter__(self):
        for e in self.entries:
            yield e

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, i):
        return self.entries[i]

    def __delitem__(self, i):
        self._remove_entry_from_ordered_dict(i)
        del self.entries[i]

    def _check(self, value):
        if not isinstance(value, self.ENTRY_TYPE):
            raise TypeError(u"Objects stored in this lexicon must have type '%s'. (Got: '%s')" % (self.ENTRY_TYPE, type(value)))

    def __setitem__(self, i, value):
        self._check(value)
        self._remove_entry_from_ordered_dict(i)
        self.entries[i] = value
        self._add_entry_to_ordered_dict(i, value)

    def insert(self, i, value):
        self._check(value)
        self.entries.insert(i, value)
        self._update_ordered_dict()

    @property
    def keys(self):
        return [e.key for e in self]

    @property
    def unique_keys(self):
        return list(self.__ordered_dict.keys())

    @property
    def has_unique_entries(self):
        return len(self) == len(self.unique_keys)

    def entries_for_key(self, key):
        try:
            return [self[i] for i in self.__ordered_dict[key]]
        except:
            return []

    def read_file(self, lexicon_file_path, comment=u"#", delimiter=u"\t", indices=[0, 1]):
        if (lexicon_file_path is None) or (not os.path.isfile(lexicon_file_path)):
            raise ValueError("The lexicon file path must exist. (Got '%s')" % lexicon_file_path)
        comment = to_unicode_string(comment)
        delimiter = to_unicode_string(delimiter)
        with io.open(lexicon_file_path, "r", encoding="utf-8") as lexicon_file:
            for line in lexicon_file:
                line = line.strip()
                if (comment is not None) and line.startswith(comment):
                    # commented line, skip
                    pass
                else:
                    acc = line.split(delimiter)
                    if len(acc) > 0:
                        self.entries.append(
                            self.ENTRY_TYPE(raw_values=[acc[i] for i in indices], lowercase=self.lowercase)
                        )
        self._update_ordered_dict()

    def shuffle(self):
        copy = list(self.entries)
        random.shuffle(copy)
        cls = type(self)
        return cls(entry_type=self.ENTRY_TYPE, entries=copy, lowercase=self.lowercase)

    def shuffle_and_partition(self, size=0.9, store=False):
        copy = list(self.entries)
        random.shuffle(copy)
        if isinstance(size, int) and size > len(copy):
            raise ValueError(u"The given size (%d) exceeds the number of entries (%d)." % (size, len(copy)))
        if isinstance(size, float):
            if (size < 0.0) or (size > 1.0):
                raise ValueError(u"The size, when expressed as a fraction, must be in [0.0, 1.0]. (Got: '%.3f')" % size)
            size = int(len(copy) * size)
        cls = type(self)
        ret = (
            cls(entries=copy[0:size], lowercase=self.lowercase),
            cls(entries=copy[size:], lowercase=self.lowercase),
        )
        if not store:
            return ret
        self.train_lexicon, self.test_lexicon = ret



