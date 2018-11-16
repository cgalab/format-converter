#!/usr/bin/python3

"""Loader for .line formatted graphs."""

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

from ORD53.graph.Graph import GeometricGraph
from ORD53.common.geometry import Vertex2
from ORD53.common.iter import pair_iterator, PeekIterator

class LineLoader:
    extension = '.line'

    """Load a graph from Martin's .line format"""
    @staticmethod
    def _add_polychain(g, f):
        """Add a single polychain from the file"""
        vertices = []
        num_elems = int(next(f))
        for _ in range(num_elems):
            (x, y) = [float(c) for c in next(f).split()]
            vertices.append(Vertex2(x, y))

        for t in pair_iterator(vertices):
            g.add_edge_by_vertex(*t)

    @classmethod
    def load(cls, f):
        """Load graph from a valid .line file"""
        g = GeometricGraph()
        f = PeekIterator(f)
        while True:
            try:
                if f.peek() == "\n":
                    next(f)
                    continue
            except StopIteration:
                break
            cls._add_polychain(g, f)
        return g

def main():
    """Load a graph from stdin or a file."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Load a graph from a .line file')
    parser.add_argument('inputfile', help='Inputfile (.line)', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outputfile', help='Outputfile (.graphml)', nargs='?', type=argparse.FileType('wb'), default=sys.stdout.buffer)
    parser.add_argument('-r', '--randomize-weights', action='store_true', default=False, help='randomize edge weights')

    args = parser.parse_args()

    g = LineLoader.load(args.inputfile)
    if args.randomize_weights:
      g.randomize_weights()
    g.write_graphml(args.outputfile)
    args.outputfile.close()
    #print(g)

if __name__ == '__main__' and __package__ is None:
    main()
