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


"""Useful additional iterators"""

#import itertools

def pair_iterator(iterable):
    """Given a list of at least two elements, return pairs of subsequent elements.

    Passing an iterator with fewer than 2 elements is considered an error.

    >>> list(pair_iterator(range(0)))
    Traceback (most recent call last):
     ...
    RuntimeError: Iterator empty
    >>> list(pair_iterator(range(1)))
    Traceback (most recent call last):
     ...
    RuntimeError: Iterator too short
    >>> list(pair_iterator(range(2)))
    [(0, 1)]
    >>> list(pair_iterator(range(3)))
    [(0, 1), (1, 2)]
    >>> list(pair_iterator(range(4)))
    [(0, 1), (1, 2), (2, 3)]
    """

    it = iter(iterable)
    try:
        prev = next(it)
    except StopIteration:
        raise RuntimeError("Iterator empty")
    i = _sentinel = object()
    for i in it:
        yield (prev, i)
        prev = i
    if i == _sentinel:
        raise RuntimeError("Iterator too short")

def cyclic_pair_iterator(iterable):
    """Given a list of at least two elements, return pairs of elements, including (last,first).

    Passing an iterator with fewer than 2 elements is considered an error.

    >>> list(cyclic_pair_iterator(range(0)))
    Traceback (most recent call last):
     ...
    RuntimeError: Iterator empty
    >>> list(cyclic_pair_iterator(range(1)))
    Traceback (most recent call last):
     ...
    RuntimeError: Iterator too short
    >>> list(cyclic_pair_iterator(range(2)))
    [(0, 1), (1, 0)]
    >>> list(cyclic_pair_iterator(range(3)))
    [(0, 1), (1, 2), (2, 0)]
    >>> list(cyclic_pair_iterator(range(4)))
    [(0, 1), (1, 2), (2, 3), (3, 0)]
    """
    it = iter(iterable)
    try:
        first = prev = next(it)
    except StopIteration:
        raise RuntimeError("Iterator empty")
    i = _sentinel = object()
    for i in it:
        yield (prev, i)
        prev = i
    if i == _sentinel:
        raise RuntimeError("Iterator too short")
    yield (prev, first)

class PeekIterator():
    """Iterator wrapper that allows peeking at the next element without removing it

    >>> list(PeekIterator(range(0)))
    []
    >>> list(PeekIterator(range(1)))
    [0]
    >>> list(PeekIterator(range(2)))
    [0, 1]
    >>> list(PeekIterator(range(3)))
    [0, 1, 2]
    """
    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self.peeked = False
        self.peeked_exception = None
        self.peeked_value = None

    def __iter__(self):
        return self

    def _return_peeked(self):
        if self.peeked_exception is not None:
            raise self.peeked_exception # pylint: disable=raising-bad-type
        else:
            return self.peeked_value

    def __next__(self):
        if self.peeked:
            self.peeked = False
            return self._return_peeked()
        else:
            return next(self.iterable)

    def peek(self):
        """Get a look at the next element.

        Return the next element without removing it from the next iterator.

        If there is no next element, forward the exception raised by
        the underlying iterator, usually a StopException.
        """
        if self.peeked:
            return self._return_peeked()
        else:
            self.peeked = True
            self.peeked_exception = None
            self.peeked_value = None
            try:
                self.peeked_value = next(self.iterable)
            except Exception as e:
                self.peeked_exception = e
                raise
            return self.peeked_value

##### code from https://docs.python.org/3/library/itertools.html#recipes
####def powerset(iterable):
####    """Compute the powerset of a list.
####
####    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
####
####    >>> list(powerset(range(0)))
####    [()]
####    >>> list(powerset(range(1)))
####    [(), (0,)]
####    >>> list(powerset(range(2)))
####    [(), (0,), (1,), (0, 1)]
####    >>> list(powerset(range(3)))
####    [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
####    >>> list(powerset([1,2,3]))
####    [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
####    """
####    s = list(iterable)
####    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))
