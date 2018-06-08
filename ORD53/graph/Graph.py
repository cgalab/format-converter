#!/usr/bin/python3

"""Module providing (geometric) graphs and operations on them"""

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

from lxml import etree as ET
from ORD53.common.IndexedSet import IndexedSet
from ORD53.common.geometry import Vertex2

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

    def __init__(self):
        self.vertices = IndexedSet()
        self.edges = set() # a set of tuples of vertex indices

    def add_vertex(self, vertex):
        """Add a vertex (instance of Vertex2) to this graph."""
        assert isinstance(vertex, Vertex2)
        return self.vertices.add(vertex)

    def add_edge_by_vertex(self, vertex0, vertex1):
        """Add an edge given by 2 vertices (instance of Vertex2) to this graph.

        Adding an edge that already exists is an error and raises a GraphException.
        """
        assert isinstance(vertex0, Vertex2)
        assert isinstance(vertex1, Vertex2)

        idx0 = self.add_vertex(vertex0)
        idx1 = self.add_vertex(vertex1)

        edge = tuple(sorted((idx0, idx1)))
        if edge in self.edges:
            raise GraphException("Edge already exists.")
        self.edges.add(tuple(sorted((idx0, idx1))))

    def __repr__(self):
        return "%s(%s, %s)"%(self.__class__.__name__, self.vertices, self.edges)

    def get_as_graphml(self):
        """Build a graphml XML document"""
        nsmap = {None : self.GRAPHML_NAMESPACE, 'xsi': self.XML_XSI}

        tags = {x: ET.QName(self.GRAPHML_NAMESPACE, x) for x in ('graphml', 'graph', 'node', 'edge', 'key', 'data')}

        graphml = ET.Element(tags['graphml'], attrib={"{"+self.XML_XSI+"}schemaLocation": self.GRAPHML_SCHEMA_LOCATION}, nsmap=nsmap)
        ET.SubElement(graphml, tags['key'], {'for': 'node', 'attr.name': 'vertex-coordinate-x', 'attr.type': 'string', 'id': 'x'})
        ET.SubElement(graphml, tags['key'], {'for': 'node', 'attr.name': 'vertex-coordinate-y', 'attr.type': 'string', 'id': 'y'})
        ET.SubElement(graphml, tags['key'], {'for': 'edge', 'attr.name': 'edge-weight', 'attr.type': 'string', 'id': 'w'})
        ET.SubElement(graphml, tags['key'], {'for': 'edge', 'attr.name': 'edge-weight-additive', 'attr.type': 'string', 'id': 'wa'})
        graph = ET.SubElement(graphml, tags['graph'], {'edgedefault': 'undirected'})

        for idx, v in enumerate(self.vertices):
            attrib = {'id': str(idx)}
            node = ET.Element(tags['node'], attrib)
            ET.SubElement(node, tags['data'], {'key': 'x'}).text = str(v.x)
            ET.SubElement(node, tags['data'], {'key': 'y'}).text = str(v.y)
            graph.append(node)

        for src, dst in self.edges:
            attrib = {'source': str(src), 'target': str(dst)}
            graph.append(ET.Element(tags['edge'], attrib))

        return graphml

    def write_graphml(self, f):
        """Write a graphml representation to the file f"""
        xml = self.get_as_graphml()
        for s in ET.tostringlist(xml, pretty_print=True):
            f.write(s)
