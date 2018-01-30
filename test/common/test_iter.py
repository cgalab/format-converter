#!/usr/bin/python3

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

import doctest
import itertools
import unittest

import ORD53.common.iter
from ORD53.common.iter import PeekIterator

def load_tests(loader, tests, pattern): # pylint: disable=unused-argument
    tests.addTests(doctest.DocTestSuite(ORD53.common.iter))
    return tests

class TestIters(unittest.TestCase):
    def test_peek_iterator(self):
        for length in range(5):
            elements = list(range(length))

            # peek in all combinations of different places between 0 and 2 times
            for peek_vector in itertools.product(*[(0, 1, 2)]*(length+1)):
                peekable = PeekIterator(elements)
                for expect, peek_cnt in zip(elements, peek_vector):
                    for _ in range(peek_cnt):
                        self.assertEqual(expect, peekable.peek())
                    self.assertEqual(expect, next(peekable))
                for _ in range(peek_vector[-1]):
                    self.assertRaises(StopIteration, peekable.peek)
                self.assertRaises(StopIteration, lambda p=peekable: next(p))


if __name__ == '__main__':
    unittest.main()
