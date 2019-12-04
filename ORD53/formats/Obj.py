#!/usr/bin/python3

# Copyright (c) 2018, 2019 Peter Palfrader
# Copyright (c) 2019 Günter Eder
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


"""Loader for .obj formatted graphs."""

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

from ORD53.graph.Graph import GeometricGraph
from ORD53.common.geometry import Vertex3
from ORD53.common.iter import pair_iterator, cyclic_pair_iterator, PeekIterator

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

    @staticmethod
    def _add_chain(g, f):
        """Add a single chain from the file"""
        temp = next(f).split()
        temp.pop(0)
        chain_list = [int(c)-1 for c in temp]
        for e in pair_iterator(chain_list):
            g.add_edge_by_index(*e, ignore_dups=True)

    @classmethod
    def load(cls, content, name="unknown", args=None):
        """Load graph from a valid .obj file"""
        g = GeometricGraph(source=name, fmt=os.path.basename(__file__))
        f = PeekIterator(content.splitlines())
        while True:
            try:
                if f.peek().startswith("v"):
                    cls._add_vertex(g, f)
                elif f.peek().startswith("f"):
                    cls._add_face(g, f)
                elif f.peek().startswith("l"):
                    cls._add_chain(g, f)
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
