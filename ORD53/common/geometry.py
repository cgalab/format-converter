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

"""2D and 3D geometric objects."""

class Vertex2:
    """A 2D Vertex

    A vertex with 2 coordinates combined with a few operators to treat it like a vector.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "%s(%.17f, %.17f)"%(self.__class__.__name__, self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)

    def __rmul__(self, scalar):
        return self.__class__(scalar * self.x, scalar * self.y)

    def dotproduct(self, other):
        """Compute the dotproduct of this vector with another one."""
        return self.x * other.x + self.y * other.y
    def lensquared(self):
        """Compute the squared length of this vector."""
        return self.dotproduct(self)


class Vertex3:
    """A 3D Vertex

    A vertex with 3 coordinates combined with a few operators to treat it like a vector.
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "%s(%.17f, %.17f, %.17f)"%(self.__class__.__name__, self.x, self.y, self.z)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rmul__(self, scalar):
        return self.__class__(scalar * self.x, scalar * self.y, scalar * self.z)

    def dotproduct(self, other):
        """Compute the dotproduct of this vector with another one."""
        return self.x * other.x + self.y * other.y + self.z * other.z
    def lensquared(self):
        """Compute the squared length of this vector."""
        return self.dotproduct(self)
