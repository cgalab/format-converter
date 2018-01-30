#!/usr/bin/python3

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
        return self.x == other.x and self.y == other.y

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
