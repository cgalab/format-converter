#!/usr/bin/python3

"""Loader for .site formatted graphs."""

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

from ORD53.graph.Graph import GeometricGraph
from ORD53.common.geometry import Vertex2
from ORD53.common.iter import pair_iterator, PeekIterator

import os

class SiteLoader:
    extension = '.site'

    @classmethod
    def load(cls, content, name="unknown", args=None):
        """Load graph from a valid .site file"""
        g = GeometricGraph(source=name, fmt=os.path.basename(__file__))
        f = iter(content.splitlines())
        while True:
            try:
                element_type = next(f).rstrip()
                element_data = next(f).rstrip()
                if element_type == "0": # segment
                    c = [float(e) for e in element_data.split()]
                    g.add_edge_by_vertex(Vertex2(c[0], c[1]), Vertex2(c[2], c[3]))
            except StopIteration:
                break
        return g

def main():
    """Load a graph from stdin or a file."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Load a graph from a .site file')
    parser.add_argument('inputfile', help='Inputfile (.site)', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outputfile', help='Outputfile (.graphml)', nargs='?', type=argparse.FileType('wb'), default=sys.stdout.buffer)
    parser.add_argument('-r', '--randomize-weights', action='store_true', default=False, help='randomize edge weights')

    args = parser.parse_args()

    g = SiteLoader.load(args.inputfile.read())
    if args.randomize_weights:
      g.randomize_weights()
    g.write_graphml(args.outputfile)
    args.outputfile.close()
    #print(g)

if __name__ == '__main__' and __package__ is None:
    main()
