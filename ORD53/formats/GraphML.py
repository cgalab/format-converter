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


"""Passthrough for .graphml formatted graphs."""

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

from ORD53.graph.Graph import GeometricGraph
from ORD53.common.geometry import Vertex2
from ORD53.common.iter import pair_iterator, PeekIterator

import os

class GraphMLPassthroughException(Exception):
    pass

class GraphMLPassthroughGraph:
    def __init__(self, content):
        self.graphml = content
        if not self.graphml.startswith('<graphml'):
            raise GraphMLPassthroughException("Not a graphml file")

    def randomize_weights(self, rnd_lower=0.0, rnd_upper=5.0):
        raise GraphMLPassthroughException("randomize_weights() not implemented for passthrough.")

    def write_graphml(self, f):
        """Write a graphml representation to the file f"""
        f.write(self.graphml.encode('UTF-8'))

class GraphMLLoader:
    extension = '.graphml'

    @classmethod
    def load(cls, content, name="unknown", args=None):
        g = GraphMLPassthroughGraph(content)
        return g
