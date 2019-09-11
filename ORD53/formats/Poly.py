#!/usr/bin/python3

"""Loader for .poly formatted graphs."""

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

from ORD53.graph.Graph import GeometricGraph
from ORD53.common.geometry import Vertex2
from ORD53.common.iter import pair_iterator, PeekIterator

from ORD53.formats.Line import LineLoader

import os

class PolyLoader:
    extension = '.poly'

    @classmethod
    def load(cls, content, name="unknown", args=None):
        """Load graph from a valid .line file"""
        g = GeometricGraph(source=name, fmt=os.path.basename(__file__))
        f = PeekIterator(content.splitlines())
        while True:
            try:
                if f.peek() == "":
                    next(f)
                    continue
            except StopIteration:
                break
            LineLoader._add_polychain(g, f, True)
            
        return g

def main():
    """Load a graph from stdin or a file."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Load a graph from a .line file')
    parser.add_argument('inputfile', help='Inputfile (.poly)', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outputfile', help='Outputfile (.graphml)', nargs='?', type=argparse.FileType('wb'), default=sys.stdout.buffer)
    parser.add_argument('-r', '--randomize-weights', action='store_true', default=False, help='randomize edge weights')

    args = parser.parse_args()

    g = PolyLoader.load(args.inputfile.read())
    if args.randomize_weights:
      g.randomize_weights()
    g.write_graphml(args.outputfile)
    args.outputfile.close()
    #print(g)

if __name__ == '__main__' and __package__ is None:
    main()
