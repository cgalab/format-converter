#!/usr/bin/python3

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

from ORD53.graph.Graph import GeometricGraph
from ORD53.common.geometry import Vertex2
from ORD53.common.iter import cyclic_pair_iterator, PeekIterator

class LineLoader:
    @staticmethod
    def _add_polychain(g, f):
        vertices = []
        num_elems = int(next(f))
        for _ in range(num_elems):
            (x, y) = [float(c) for c in next(f).split()]
            vertices.append(Vertex2(x, y))

        for t in cyclic_pair_iterator(vertices):
            g.add_edge_by_vertex(*t)

    @classmethod
    def load(cls, f):
        g = GeometricGraph()
        f = PeekIterator(f)
        while True:
            try:
                if f.peek() == "\n":
                    continue
            except StopIteration:
                break
            cls._add_polychain(g, f)
        return g

def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Load a graph from a .line file')
    parser.add_argument('inputfile', help='Inputfile (.line)', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()

    g = LineLoader.load(args.inputfile)
    print(g)

if __name__ == '__main__' and __package__ is None:
    main()
