#!/usr/bin/python3

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
    # pylint: disable=too-few-public-methods
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
