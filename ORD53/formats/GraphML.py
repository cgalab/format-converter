#!/usr/bin/python3

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
