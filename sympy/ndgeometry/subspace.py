"""Unbounded subspace that can be embedded within the global space or
another subspace.

Contains
========
Subspace

"""

from __future__ import print_function, division

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

from sympy import sympify
from sympy.core import S
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
        if len(coords) > parent_space.order:
            raise ValueError('Cannot have more coordinates than are in the '
                             'parent parameter space.')
        params = Tuple(*sympify(params))
        for p in params:
            if not p.is_Symbol:
                raise ValueError("Parameter argument must be list of Symbols, "
                                 "not %s" % p)
        obj = BaseSpace.__new__(cls, coords, params, parent_space, **kwargs)
        return obj

    @property
    def coords(self):
        return self.args[0]
    @property
    def params(self):
        return self.args[1]
    @property
    def parent_space(self):
        return self.args[2]

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

    def in_ancestor(self, n=S.Infinity):
        """Create equivalent subspace in the coordinates of the nth ancestor.

        The zeroth ancestor is this space's parent, so space.is_ancestor(0)
        will always be equal to space.  If n is sufficiently large, a new
        subspace will be returned as a child of global_space.

        """
        if n == S.Zero or self.parent_space == global_space:
            return self
        new_coords = self.parent_space.coords.subs(
            zip_longest(self.parent_space.params, self.coords, fillvalue=0))
        return Subspace(new_coords, self.params,
                        self.parent_space.parent_space).in_ancestor(n-1)
