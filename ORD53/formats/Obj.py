#!/usr/bin/python3

"""Loader for .obj formatted graphs."""

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

from ORD53.graph.Graph import GeometricGraph
from ORD53.common.geometry import Vertex3
from ORD53.common.iter import cyclic_pair_iterator, PeekIterator

import os

class ObjLoader:
    extension = '.obj'

    """Load a graph from a Wavefront OBJ format"""
    @staticmethod
    def _add_vertex(g, f):
        """Add a single vertex from the file"""
        (v, x, y, z) = [c for c in next(f).split()]
        g.add_vertex(Vertex3(float(x), float(y), float(z)))
    
    @staticmethod
    def _add_face(g, f):
        """Add a single face from the file"""
        temp = next(f).split()
        temp.pop(0)
        face_list = [int(c)-1 for c in temp]
        for e in cyclic_pair_iterator(face_list):
            g.add_edge_by_index(*e, ignore_dups=True)

    @classmethod
    def load(cls, content, name="unknown", args=None):
        """Load graph from a valid .line file"""
        g = GeometricGraph(source=name, fmt=os.path.basename(__file__))
        f = PeekIterator(content.splitlines())
        while True:
            try:
                if f.peek().startswith("v"):
                    cls._add_vertex(g, f)
                elif f.peek().startswith("f"):
                    cls._add_face(g, f)
                else:
                    next(f)

            except StopIteration:
                break
        return g

def main():
    """Load a graph from stdin or a file."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Load a graph from a .obj file')
    parser.add_argument('inputfile', help='Inputfile (.obj)', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outputfile', help='Outputfile (.graphml)', nargs='?', type=argparse.FileType('wb'), default=sys.stdout.buffer)
    parser.add_argument('-r', '--randomize-weights', action='store_true', default=False, help='randomize edge weights')

    args = parser.parse_args()

    g = ObjLoader.load(args.inputfile.read())
    if args.randomize_weights:
      g.randomize_weights()
    g.write_graphml(args.outputfile)
    args.outputfile.close()
    #print(g)

if __name__ == '__main__' and __package__ is None:
    main()
