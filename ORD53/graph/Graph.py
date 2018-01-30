#!/usr/bin/python3

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

#import pygraphml
from ORD53.common.IndexedSet import IndexedSet
from ORD53.common.geometry import Vertex2

class GeometricGraph:
    def __init__(self):
        self.vertices = IndexedSet()
        self.edges = set() # a set of tuples of vertex indices

    def add_vertex(self, vertex):
        assert isinstance(vertex, Vertex2)
        return self.vertices.add(vertex)

    def add_edge_by_vertex(self, vertex0, vertex1):
        assert isinstance(vertex0, Vertex2)
        assert isinstance(vertex1, Vertex2)

        idx0 = self.add_vertex(vertex0)
        idx1 = self.add_vertex(vertex1)

        self.edges.add(tuple(sorted((idx0, idx1))))

    def __repr__(self):
        return "%s(%s, %s)"%(self.__class__.__name__, self.vertices, self.edges)
