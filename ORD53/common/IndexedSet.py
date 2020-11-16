#!/usr/bin/python3

# Copyright (c) 2018, 2019 Peter Palfrader
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""This module provides the IndexedSet class."""

class IndexedSet:
    """A set of elements backed by a list

    Since it's a set, each (hash) value may exist at most once.

    Item deletion is not supported, indices stay stable."""
    def __init__(self):
        self.list = []
        self.key_to_idx = {}

    def add(self, item):
        """Adds item to the set if it does not yet exist.  Returns its index in both cases."""
        try:
            return self.key_to_idx[item]
        except KeyError:
            idx = len(self.list)
            self.list.append(item)
            self.key_to_idx[item] = idx
            return idx

    def __iter__(self):
        yield from self.list

    def __repr__(self):
        return "%s(%s)"%(self.__class__.__name__, self.list)

    def __len__(self):
        return len(self.list)
