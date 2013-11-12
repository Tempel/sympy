"""Contains the definition of a global space, plus one instance of such.

"""

from __future__ import print_function, division

from itertools import count

from sympy.core import S
from sympy.core.compatibility import as_int
from sympy.core.containers import Tuple
from sympy.core.symbol import Symbol

from sympy.ndgeometry.base_space import BaseSpace


class GlobalSpace(BaseSpace):
    """An infinite-dimensional rectilinear space.

    Any global space has an infinite number of dimensions, accessible by
    indexing.  For convenience, the first three dimensions can be accessed as
    attributes x, y, and z, respectively.

    """

    order = S.Infinity

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start if index.start is not None else 0
            step = index.step if index.step is not None else 1
            if index.stop is None:
                raise ValueError('Cannot slice to end; global space has '
                                 'infinite dimensions.')
            return Tuple(*(self[j] for j in
                           range(start, index.stop, step)))
        return Symbol('Global{0}'.format(as_int(index)))
    def __iter__(self):
        return (self[i] for i in count())

    @property
    def params(self):
        return self
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
