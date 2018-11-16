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

class IpeLoader:
    """Load a graph from an IPE file"""
    extension = '.ipe'

    @staticmethod
    def _transform(x, y, matrix):
        """Transform a point (x,y) as defined by matrix."""
        if matrix is None:
            return x, y

        m = map(lambda a: float(a), matrix.split())
        if len(m) != 6:
            raise("Invalid matrix '%s'."%(matrix))

        x, y = x*m[0] + y*m[2], x*m[1] + y*m[3]

        x += m[4]
        y += m[5]
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
    def load(cls, f):
        """Load graph from a valid .line file"""
        g = GeometricGraph()
        tree = ET.parse(f)
        root = tree.getroot()

        for e in root.findall("./page/path"):
            t =  e.text
            m = e.attrib['matrix'] if 'matrix' in e.attrib else None
            #p = e.attrib['pen'] if 'pen' in e.attrib else None
            #speed = None
            #if 'stroke' in e.attrib:
            #    s = e.attrib['stroke'].split(' ', 2)
            #    if len(s) == 3:
            #        blue = float(s[2])
            #        speed = (0.502 * 2)/(1-blue) - 1
            cls._add_path(g, t, m)
        return g

def main():
    """Load a graph from stdin or a file."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Load a graph from an .ipe file')
    parser.add_argument('inputfile', help='Inputfile (.ipe)', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outputfile', help='Outputfile (.graphml)', nargs='?', type=argparse.FileType('wb'), default=sys.stdout.buffer)
    parser.add_argument('-r', '--randomize-weights', action='store_true', default=False, help='randomize edge weights')

    args = parser.parse_args()

    g = IpeLoader.load(args.inputfile)
    if args.randomize_weights:
      g.randomize_weights()
    g.write_graphml(args.outputfile)
    args.outputfile.close()
    #print(g)

if __name__ == '__main__' and __package__ is None:
    main()
