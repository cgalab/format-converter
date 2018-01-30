#!/usr/bin/python3

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
