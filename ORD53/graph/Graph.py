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


"""Module providing (geometric) graphs and operations on them"""

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

from lxml import etree as ET
from ORD53.common.IndexedSet import IndexedSet
from ORD53.common.geometry import Vertex2, Vertex3
import os
import random
import sys

class GraphException(Exception):
    """Exception raised by classes in this module."""
    pass

class GeometricGraph:
    """A geometric graph.

    This is a graph where vertices have (2d) coordinates.
    """

    GRAPHML_NAMESPACE = 'http://graphml.graphdrawing.org/xmlns'
    XML_XSI = 'http://www.w3.org/2001/XMLSchema-instance'
    GRAPHML_SCHEMA_LOCATION = 'http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd'

    DEFAULT_W = str(1.0)
    DEFAULT_WA = str(0.0)

    def __init__(self, source="unknown", fmt=None):
        self.vertices = IndexedSet()
        self.edges = {}
        self.source = source
        self.fmt = fmt

    def add_vertex(self, vertex):
        """Add a vertex (instance of Vertex2 or Vertex3) to this graph."""
        assert isinstance(vertex, (Vertex2, Vertex3))
        return self.vertices.add(vertex)

    def add_edge_by_index(self, idx0, idx1, w=None, wa=None, ignore_dups=False):
        """Add an edge given by 2 vertices (instance of int) to this graph."""
        assert isinstance(idx0, int)
        assert isinstance(idx1, int)

        edge = tuple(sorted((idx0, idx1)))
        if edge in self.edges and not ignore_dups:
            raise GraphException("Edge already exists.")
        self.edges[edge] = {
            'w': w,
            'wa': wa
        }

    def add_edge_by_vertex(self, vertex0, vertex1, w=None, wa=None):
        """Add an edge given by 2 vertices (instance of Vertex2) to this graph.

        Adding an edge that already exists is an error and raises a GraphException.
        """
        assert isinstance(vertex0, (Vertex2, Vertex3))
        assert isinstance(vertex1, (Vertex2, Vertex3))

        idx0 = self.add_vertex(vertex0)
        idx1 = self.add_vertex(vertex1)

        edge = tuple(sorted((idx0, idx1)))
        if idx0 == idx1:
            print("Ignoring loop edge", edge, file=sys.stderr)
            return
        if edge in self.edges:
            raise GraphException("Edge already exists.")
        self.edges[edge] = {
            'w': w,
            'wa': wa
        }

    def __repr__(self):
        return "%s(%s, %s)"%(self.__class__.__name__, self.vertices, self.edges)

    def randomize_weights(self, rnd_lower=0.20, rnd_upper=5.0, round_n=None):
        for k, v in self.edges.items():
            while True:
              r = random.uniform(rnd_lower, rnd_upper);
              if round_n == 0:
                  r = round(r)  # So this gets turned into an integer, unlike when calling round(r,0)
              elif round_n is not None:
                  r = round(r, round_n)
              if r != 0: break
            v['w'] = str(r)

    def transform_coordinates(self, scale=None):
        if scale is not None:
            new_v = IndexedSet()
            for v in self.vertices:
                assert isinstance(v, (Vertex2, Vertex3))
                new_v.add( scale * v )
            self.vertices = new_v

    def get_nsmap(self):
        return {None : self.GRAPHML_NAMESPACE, 'xsi': self.XML_XSI}

    def get_tags(self):
        return {x: ET.QName(self.GRAPHML_NAMESPACE, x) for x in ('graphml', 'graph', 'node', 'edge', 'key', 'data', 'default')}

    def get_as_graphml(self):
        """Build a graphml XML document"""
        nsmap = self.get_nsmap()
        tags = self.get_tags()

        graphml = ET.Element(tags['graphml'], attrib={"{"+self.XML_XSI+"}schemaLocation": self.GRAPHML_SCHEMA_LOCATION}, nsmap=nsmap)
        ET.SubElement(graphml, tags['key'], {'for': 'node', 'attr.name': 'vertex-coordinate-x', 'attr.type': 'string', 'id': 'x'})
        ET.SubElement(graphml, tags['key'], {'for': 'node', 'attr.name': 'vertex-coordinate-y', 'attr.type': 'string', 'id': 'y'})
        key = ET.SubElement(graphml, tags['key'], {'for': 'edge', 'attr.name': 'edge-weight', 'attr.type': 'string', 'id': 'w'})
        ET.SubElement(key, tags['default']).text = self.DEFAULT_W;
        key = ET.SubElement(graphml, tags['key'], {'for': 'edge', 'attr.name': 'edge-weight-additive', 'attr.type': 'string', 'id': 'wa'})
        ET.SubElement(key, tags['default']).text = self.DEFAULT_WA;
        graph = ET.SubElement(graphml, tags['graph'], {'edgedefault': 'undirected'})

        for idx, v in enumerate(self.vertices):
            attrib = {'id': str(idx)}
            node = ET.Element(tags['node'], attrib)
            ET.SubElement(node, tags['data'], {'key': 'x'}).text = str(v.x)
            ET.SubElement(node, tags['data'], {'key': 'y'}).text = str(v.y)
            graph.append(node)

        for edge, attributes in self.edges.items():
            src, dst  = edge
            attrib = {'source': str(src), 'target': str(dst)}
            edge = ET.Element(tags['edge'], attrib)
            if attributes['w'] is not None:
                ET.SubElement(edge, tags['data'], {'key': 'w'}).text = str(attributes['w'])
            if attributes['wa'] is not None:
                ET.SubElement(edge, tags['data'], {'key': 'wa'}).text = attributes['wa']
            graph.append(edge)

        commenttext = " Created by %s from %s "%(os.path.basename(sys.argv[0]), self.source)
        commenttext = commenttext.replace('--', '- -')
        if self.fmt is not None:
            commenttext += " [%s]"%(self.fmt)
        comment = ET.Comment(commenttext)
        graphml.insert(0, comment)
        return graphml

    def write_graphml(self, f):
        """Write a graphml representation to the file f"""
        xml = self.get_as_graphml()
        for s in ET.tostringlist(xml, pretty_print=True):
            f.write(s)

    def write_ipe(self, f, markers=False):
        f.write("""<?xml version="1.0"?>
<!DOCTYPE ipe SYSTEM "ipe.dtd">
<ipe version="70000" creator="surfer2">
<info bbox="cropbox" />
<ipestyle name="basic">
<symbol name="mark/disk(sx)" transformations="translations">
<path fill="sym-stroke">
0.6 0 0 0.6 0 0 e
</path>
</symbol>
</ipestyle>
<ipestyle name="surf">
  <color name="black" value="0 0 0"/>
  <color name="gray" value="0.2 0.2 0.2"/>
  <color name="blue" value="0 0 1"/>
  <color name="royalblue" value="0 0.5 1"/>
  <color name="magenta" value="1 0 1"/>
  <color name="red" value="1 0 0"/>
  <color name="darkgreen" value="0 0.5 0"/>
  <color name="orange" value="1 0.66 0.34"/>
</ipestyle>
<page>
<layer name="edges"/>
""".encode())
        if markers:
            f.write("""<layer name="vertices"/>\n""".encode())
        for vi1, vi2 in self.edges.keys():
            v1 = self.vertices.list[vi1]
            v2 = self.vertices.list[vi2]
            f.write(("""<path layer="edges">
    %s %s m
    %s %s l
  </path>
"""%(v1.x,v1.y,v2.x,v2.y)).encode())

        if markers:
            for v in self.vertices.list:
                f.write(("""<use layer="vertices" name="mark/disk(sx)" pos="%s %s" size="normal" stroke="black"/>\n"""%(v.x, v.y)).encode())
        f.write("</page>\n</ipe>\n".encode())

    def write_obj(self, f, zero_offset = False):
        offset = 1 if not zero_offset else 0
        f.write("""# wavefront obj file\n""".encode())
        for v in self.vertices.list:
            f.write(("""v %s %s %s\n"""%(v.x, v.y, str(0.0))).encode())
        for vi1, vi2 in self.edges.keys():
            f.write(("""f %s %s\n"""%(vi1+offset,vi2+offset)).encode())
