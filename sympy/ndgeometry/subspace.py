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

    A space that exists embedded within another space.  It can have as many
    coordinate functions as its parent space has parameters; if any functions
    are not defined, their coordinates are assumed to be zero.

    Parameters
    ==========
    coords : list of SymPy expressions
        The parametric functions that defines where the subspace exists.
    params : list of Symbols
        The symbols of the parametric functions that represent where the
        subspace exists.
    parent_space : Subspace, optional
        The space in which this subspace's coordinates are defined.
        Defaults to the global_space.

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
