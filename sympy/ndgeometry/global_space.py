"""Contains the definition of a global space, plus one instance of such.

"""

from __future__ import print_function, division

from sympy.core.symbol import Symbol
from sympy.ndgeometry.base_space import BaseSpace

class GlobalSpace(BaseSpace):
    """An infinite-dimensional rectilinear space.

    Any global space has an infinite number of dimensions, accessible by
    indexing.  For convenience, the first three dimensions can be accessed as
    attributes x, y, and z, respectively.

    """

    def __getitem__(self, index):
        return Symbol('Global{0}'.format(index))
    @property
    def x(self):
        return self[0]
    @property
    def y(self):
        return self[1]
    @property
    def z(self):
        return self[2]

    def is_descendant(self, other):
        return self == other


global_space = GlobalSpace()
