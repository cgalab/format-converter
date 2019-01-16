#!/usr/bin/python3

"""Loader for .ipe files."""

if __name__ == '__main__' and __package__ is None:
    import os
    __LEVEL = 2
    os.sys.path.append(os.path.abspath(os.path.join(*([os.path.dirname(__file__)] + ['..']*__LEVEL))))

from ORD53.graph.Graph import GeometricGraph
from ORD53.common.geometry import Vertex2
from ORD53.common.iter import pair_iterator, PeekIterator

import xml.etree.ElementTree as ET
import os

class IpeLoader:
    """Load a graph from an IPE file"""
    extension = '.ipe'

    @staticmethod
    def _transform(x, y, matrix):
        """Transform a point (x,y) as defined by matrix."""
        if matrix is None:
            return x, y

        if len(matrix) != 6:
            raise("Invalid matrix '%s'."%(matrix))

        x, y = x*matrix[0] + y*matrix[2], x*matrix[1] + y*matrix[3]

        x += matrix[4]
        y += matrix[5]
        return x, y

    @staticmethod
    def _sample_arc(g, center, r, v0, v1):
        mx = center[0]
        my = center[1]

        vec0x = -mx + v0.x
        vec0y = -my + v0.y

        vec1x = -mx + v1.x
        vec1y = -my + v1.y

        sp = vec0x*vec1x + vec0y*vec1y
        l0 = math.sqrt(vec0x*vec0x + vec0y*vec0y)
        l1 = math.sqrt(vec1x*vec1x + vec1y*vec1y)

        angle = math.acos( sp / (l0*l1) )

        samplepoints = [ v0 ]
        samples = 32
        for i in xrange(1, samples):
            d = angle * (float(i)/samples)
            vx = vec0x * math.cos(d) - vec0y * math.sin(d);
            vy = vec0x * math.sin(d) + vec0y * math.cos(d);

            x = mx + vx
            y = my + vy

            samplepoints.append( Vertex2(x, y) )

        samplepoints.append( v1 )

        for t in pair_iterator(samplepoints):
            g.add_edge_by_vertex(*t)

    @staticmethod
    def _add_path(g, t, matrix = None, speed = None, wa = None):
        """Add a single path object"""
        lines = []
        for l in t.split("\n"):
            if l == "": continue
            lines.append(l)

        if len(lines) < 2:
            raise Exception("less than two lines in path block")

        line = lines.pop(0)
        f = line.split()
        if f[2] != "m":
            raise Exception("first line of text did not start with an m element")
        x, y = float(f[0]), float(f[1])
        x, y = IpeLoader._transform(x, y, matrix)
        v0 = Vertex2(x, y)
        first = v0

        while len(lines) > 0:
            line = lines.pop(0)
            if line == "h":
                if (len(lines) != 0):
                    raise Exception("Found 'h' in path but not at the end.   Confused.")
                v1 = first
                pathtype = 'l'
            else:
                f = line.split()
                x, y = float(f[0]), float(f[1])
                x, y = IpeLoader._transform(x, y, matrix)
                pathtype = f[-1]
                if pathtype == "l":
                    v1 = Vertex2(x, y)

            if pathtype == "l":
                e = { "vertex0": v0, "vertex1": v1 }
                if speed is not None:
                    e['w'] = speed
                if wa is not None:
                    e['wa'] = wa
                g.add_edge_by_vertex(**e)
                v0 = v1
            elif pathtype == "a":
                if matrix is not None:
                    raise Exception("Cannot handle matrix transformed arcs yet")
                if len(lines) > 0:
                    raise Exception("More lines after arc in line block?")
                if f[0] != f[3] or f[1] != '0' or f[2] != '0':
                    raise Exception("Arc not a circle? " + ' '.join(f))

                center = (float(f[4]), float(f[5]))
                r = f[0];
                v1 = Vertex2(float(f[6]), float(f[7]))
                IpeLoader._sample_arc(g, center, r, v0, v1)
            else:
                raise Exception("Unknown element in second line of text")




    @classmethod
    def load(cls, content, name="unknown", args=None):
        """Load graph from a valid .line file"""
        flatten = args is not None and args.flatten

        root = ET.fromstring(content)
        graph = GeometricGraph(name, fmt=os.path.basename(__file__)) if flatten else None
        graphs = []

        for child in root:
            if child.tag != "page": continue
            page = child

            if not flatten:
                layer_visible_in_views = {}
                for v in page.findall("./view"):
                    g = GeometricGraph(source="%s (view %d)"%(name, len(graphs)+1), fmt=os.path.basename(__file__))
                    graphs.append(g)
                    if 'layers' not in v.attrib: continue

                    for l in v.attrib['layers'].split():
                        if not l in layer_visible_in_views:
                            layer_visible_in_views[l] = []
                        layer_visible_in_views[l].append(g)

            active_layer = None
            for child in page:
                if 'layer' in child.attrib:
                    active_layer = child.attrib['layer']
                if child.tag != 'path': continue

                t =  child.text
                m = list(map(lambda a: float(a), child.attrib['matrix'].split())) if 'matrix' in child.attrib else None
                #p = child.attrib['pen'] if 'pen' in child.attrib else None
                #speed = None
                #if 'stroke' in child.attrib:
                #    s = child.attrib['stroke'].split(' ', 2)
                #    if len(s) == 3:
                #        blue = float(s[2])
                #        speed = (0.502 * 2)/(1-blue) - 1
                if active_layer is None:
                    raise Exception("No active layer.")
                if flatten:
                    cls._add_path(graph, t, m)
                else:
                    if not active_layer in layer_visible_in_views:
                        continue
                    assert(isinstance(layer_visible_in_views[active_layer], list))
                    for g in layer_visible_in_views[active_layer]:
                        assert(isinstance(g, GeometricGraph))
                        cls._add_path(g, t, m)

        if flatten:
            return graph
        else:
            return graphs

def main():
    """Load a graph from stdin or a file."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Load a graph from an .ipe file')
    parser.add_argument('inputfile', help='Inputfile (.ipe)', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outputfile', help='Outputfile (.graphml)', nargs='?', type=argparse.FileType('wb'), default=sys.stdout.buffer)
    parser.add_argument('-r', '--randomize-weights', action='store_true', default=False, help='randomize edge weights')
    parser.add_argument('-f', '--flatten', action='store_true', default=False, help='flatten views and pages')

    args = parser.parse_args()

    g = IpeLoader.load(args.inputfile.read())
    if not isinstance(g, list):
        g = [g]
    if args.randomize_weights:
      for i in g:
        i.randomize_weights()
    for i in g:
        i.write_graphml(args.outputfile)
    args.outputfile.close()
    #print(g)

if __name__ == '__main__' and __package__ is None:
    main()
