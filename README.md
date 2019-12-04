# format converter

This tool converts from various formats of planar straight-line graphs
used in our research groups to the [GraphML] format used by our straight
skeleton codes [monos] and [surfer2].

The specification can be found in the [GRAPH-ATTRIBUTES][./GRAPH-ATTRIBUTES.md]
in this repository.

[monos]: https://github.com/cgalab/monos/
[surfer2]: https://github.com/cgalab/surfer/
[graphml]: http://graphml.graphdrawing.org/

# Installing

Just symlinking `bin/ord-format` to your `~/bin` directory, if that is in your
`PATH` should suffice.  If you want a more pythonesque way, then `pip3 install .`
or `pip3 install -e .` should also work.

# Running

The main interface is the `ord-format` script which reads from one file and
writes the resulting .graphml to a file or `stdout`.  The `-r` option adds
random edge weights.

For testing purposes, some of the readers can also be run individually,
as in `python3 ./ORD53/formats/Line.py ../test-data/st0000054.line st0000054.graphml'.

# Supported input formats

There is no formal specification for many of the formats in use here.  Here we
list the ones that format-converter is able to read, along with a brief
description of how they look.  All file formats, unless otherwise stated, are
text formats and (text-) line based.

## `.line`

A `.line` file consists of one or more blocks of the following:  A line with an
integer specifying the number of vertices in the following, then a list of that
many text-lines of x and y coordinates, and lastly an empty line.  Coordinates
in a line are space seperated; there may be leading whitespace.

Each such block is considered a polygonal chain.  For closed chains, the first
vertex is repeated at the end (and also counted as a vertex).

For polygons, it is customary to have its boundary in positive (i.e., counter
clockwise) orientation.  Any holes would be subsequent blocks in negative orientation.

## `.poly` (deprecated)

A `.poly` file is a `.line` file in which the line segments implicitly form a
closed chain.  That is, unlike with `.line`, the first vertex in the list is
not repeated at the end.

## `.site`

Site files can represent line segments, (isolated) points, and circular arc
pieces.  The format is a sequence of line-pairs, the first specifying the type
and the second providing data for the element.  Element-type 0 for instance is a
line segment, element-type 2 an isolated point.  -1 and 1 are circular arc
segments.  The only element-type supported is 2, a line segment.  Its data
line consists of a 4-tuple (x0, y0, x1, y1) where (x0,y0) and (x1,y1) are
the coordinates of the segments endpoints.

## `.obj`

[Wavefront OBJ][obj] files first specify a list of vertices, and then faces or
polygonal chains that refer to these vertices by index (1-based).

Currently format converter can read chain based (`l <idx> <idx> ...`) and face
based (`f <idx> <idx> <idx> ...`) `.obj` files with only positive vertex
indices.

These files are also understood by [blender] which makes them a nice
interchange format at times.

[obj]: https://www.fileformat.info/format/wavefrontobj/egff.htm
[blender]: https://www.blender.org/

## `.ipe`

[IPE] is a popular drawing program in our community.  It allows storing
drawings in `.pdf` files to be directly included in LaTeX documents while still
being able to edit them afterwards.  The format converter can parse (simple)
.ipe files and extract line segments from it.

The pen width, when numerically assigned to segments in the drawing, is
interpreted as edge weight.

[ipe]: http://ipe.otfried.org/

