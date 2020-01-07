#!/usr/bin/python3

# Copyright (c) 2018, 2019, 2020 Peter Palfrader
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

class GraphMLLoader:
    extension = '.graphml'

    @staticmethod
    def _load_graphml(g, content):
        try:
            import pygraphml
        except ModuleNotFoundError as e:
            print("Warning: To read graphml files we need the pygraphml module.")
            return

        parser = pygraphml.GraphMLParser()
        gml = parser.parse_string(content)
        vertices = {}
        for node in gml.nodes():
            vertices[node.id] = Vertex2(node['x'], node['y'])

        for edge in gml.edges():
            weigth = None
            try:
                weigth = edge['w']
            except KeyError:
                pass
            g.add_edge_by_vertex( vertices[ edge.parent().id ], vertices[ edge.child().id ], w=weigth)

    @classmethod
    def load(cls, content, name="unknown", args=None):
        g = GeometricGraph(source=name, fmt=os.path.basename(__file__))
        cls._load_graphml(g, content)

        return g
