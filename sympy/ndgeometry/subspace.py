"""Unbounded subspace that can be embedded within the global space or
another subspace.

Contains
========
Subspace

"""

from __future__ import print_function, division

from sympy import sympify
from sympy.ndgeometry.base_space import BaseSpace
from sympy.ndgeometry.global_space import global_space

class Subspace(BaseSpace):
    """Unbounded subspace.

    """

    def __new__(cls, coords, params, parent_space=global_space, **kwargs):
        coords = sympify(coords)
        params = sympify(params)
        obj = BaseSpace.__new__(cls, coords, params, parent_space, **kwargs)
        obj.coords = coords
        obj.params = params
        obj.parent_space = parent_space
        return obj

    @property
    def order(self):
        "The dimensionality of this subspace."
        return len(self.params)
