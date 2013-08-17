"""Unbounded subspace that can be embedded within the global space or
another subspace.

Contains
========
Subspace

"""

from __future__ import print_function, division

from sympy import sympify
from sympy.core.containers import Tuple

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
        coords = Tuple(*sympify(coords))
        params = Tuple(*sympify(params))
        for p in params:
            if not p.is_Symbol:
                raise ValueError("Parameter argument must be list of Symbols, "
                                 "not %s" % p)
        obj = BaseSpace.__new__(cls, coords, params, parent_space, **kwargs)
        obj.coords = coords
        obj.params = params
        obj.parent_space = parent_space
        return obj

    @property
    def order(self):
        """The dimensionality of this subspace."""
        return len(self.params)

    def __contains__(self, other):
        """Determine if another subspace lies entirely within this subspace.

        Returns
        =======
        A SymPy And object containing any number of SymPy Equality objects.
        This will indicate how Symbols need to be constrained in order for
        the other subspace to be entirely within this subspace.  This will
        reduce to True or False whenever those Symbols can be more thoroughly
        constrained.

        """
        # If this space is an ancestor of the other, the other subspace will
        # definitely be in this subspace.
        if other.is_descendant(self):
            return True
        # Otherwise... give up.
        raise NotImplementedError('This currently works only for direct '
                                  'ancestors.')

    def _eval_subs(self, old, new):
        """Create new subspace by substituting symbols in coordinate functions.

        """
        new_coords = self.coords.subs(old, new)
        new_parent = self.parent_space.subs(old, new)
        return Subspace(new_coords, self.params, new_parent)
