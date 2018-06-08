# ORD53 attributes for graphml graphs.

The basic graphs represented by [graphml] are abstract graphs, that is, we
store just vertices and edges.  Edges are unordered tuples of vertices,
and vertices only have an identifier, which is used in the edge
definitions, but no additional information on top of that.

While graphml allows for directed graphs, nested graphs, more than one
graph per file, and other things, we don't use any of that here.

The graphml format also defines a means to add additional attributes
to graph elements such as vertices and edges.

We define the following attributes for vertices.
*  vertex-coordinate-x: The X-coordinate of this vertex.
   The data type of this attribute can either be double or string.
*  vertex-coordinate-y: The Y-coordinate of this vertex.
   The data type of this attribute can either be double or string.

We define the following attributes for edges.
*  edge-weight: The (multiplicative) weight of this edge.
   The data type of this attribute can either be double or string.
*  edge-weight-additive: The (additive) weight of this edge.
   The data type of this attribute can either be double or string.

# see also

* [GraphML Primer][graphml-primer]
* [GraphML Specification][graphml-spec]

[graphml]: http://graphml.graphdrawing.org/
[graphml-primer]: http://graphml.graphdrawing.org/primer/graphml-primer.html
[graphml-spec]: http://graphml.graphdrawing.org/specification.html
