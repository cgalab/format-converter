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

from lxml import etree as ET

from ORD53.graph.Graph import GeometricGraph
from ORD53.common.IndexedSet import IndexedSet
from ORD53.common.geometry import Vertex2
from ORD53.common.iter import pair_iterator, PeekIterator

import os
import sys

class GraphMLLoader:
    extension = '.graphml'

    @staticmethod
    def _load_item(item, keys, tags):
        item_attrs = {}
        for data in item:
            if data.tag != tags['data']: continue
            if not 'key' in data.attrib: raise Exception("data has no key!")
            k = data.attrib['key']
            if not k in keys: raise Exception("Unknown key " + k)
            item_attrs[k] = data.text

        res = {}
        for k in keys:
            if k in item_attrs: value = item_attrs[k]
            else: value = keys[k]['default']
            if value is not None:
                res[keys[k]['attr.name']] = value
        return res

    @staticmethod
    def _load_graphml(source, fmt, content):
        graphs = []
        g = GeometricGraph(source=source, fmt=fmt)
        tags = g.get_tags()

        root = ET.fromstring(content.encode())
        if not root.tag == tags['graphml']:
            raise Exception("Not a graphml file")

        keys_attrs_edge = {}
        keys_attrs_node = {}

        for child in root:
            if child.tag != tags['key']: continue

            a = None
            if child.attrib['for'] == "node": a = keys_attrs_node
            if child.attrib['for'] == "edge": a = keys_attrs_edge
            if a is not None:
                h = { 'attr.name': child.attrib['attr.name'] }
                default = child.find(tags['default'])
                if default is not None:
                    h['default'] = default.text
                a[child.attrib['id']] = h
            else:
                print("Ignoring unknown key", ET.tostring(child), file=sys.stderr)

        for graph in root:
            if graph.tag != tags['graph']: continue

            vertices = {}
            for child in graph:
                if child.tag != tags['node']: continue
                if not 'id' in child.attrib: raise Exception("Node has no id!")

                id = child.attrib['id']
                node_data = GraphMLLoader._load_item(child, keys_attrs_node, tags)
                if not 'vertex-coordinate-x' in node_data: raise Exception("No vertex-coordinate-x for node")
                if not 'vertex-coordinate-y' in node_data: raise Exception("No vertex-coordinate-y for node")
                vertices[id] = g.add_vertex( Vertex2(node_data['vertex-coordinate-x'], node_data['vertex-coordinate-y']) )

            for child in graph:
                if child.tag != tags['edge']: continue
                if not 'source' in child.attrib: raise Exception("Edge has no source!")
                if not 'target' in child.attrib: raise Exception("Edge has no target!")

                idx0 = vertices[ child.attrib['source'] ]
                idx1 = vertices[ child.attrib['target'] ]

                edge_data = GraphMLLoader._load_item(child, keys_attrs_edge, tags)
                w = edge_data.get('edge-weight', None)
                wa = edge_data.get('edge-weight-additive', None)
                if w == g.DEFAULT_W: w = None
                if wa == g.DEFAULT_WA: wa = None
                g.add_edge_by_index(idx0, idx1, w=w, wa=wa)

            graphs.append(g)
            g = GeometricGraph(source=source, fmt=fmt)
        return graphs

    @classmethod
    def load(cls, content, name="unknown", args=None):
        g = cls._load_graphml(source=name, fmt=os.path.basename(__file__), content=content)

        return g
