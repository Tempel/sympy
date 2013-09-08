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
from sympy.core.relational import Equality
from sympy.logic.boolalg import And

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
    implicit: SymPy Boolean expression, optional
        Some expression (e.g. And, Equality) that is True if and only if a
        subspace is contained entirely within this subspace.  Note that
        these are not checked against the coordinate equations to ensure
        correctness.
    inverse: list of SymPy expressions, optional
        A set of equations that convert coordinates in the parent subspace
        to coordinates in this subspace.  The inverse of the coordinate
        equations above.  Requires an implicit equation in order to first
        determine if the parent space coordinates are actually within this
        space.  Note that these are not checked against the coordinate
        equations to ensure they match.

    """

    def __new__(cls, coords, params, parent_space=global_space, implicit=None,
                inverse=None, **kwargs):
        coords = Tuple(*sympify(coords))
        if len(coords) > parent_space.order:
            raise ValueError('Cannot have more coordinates than are in the '
                             'parent parameter space.')
        params = Tuple(*sympify(params))
        for p in params:
            if not p.is_Symbol:
                raise ValueError("Parameter argument must be list of Symbols, "
                                 "not %s" % p)
        if implicit is not None:
            if parent_space != global_space and parent_space.inverse is None:
                raise ValueError('Can only use implicit definitions if parent '
                                 'space has inverse functions.')
        if inverse is not None:
            if implicit is None:
                raise ValueError('Implicit equations are required in order to '
                                 'have inverse equations.')
            inverse = Tuple(*inverse)
            if len(inverse) != len(params):
                raise ValueError('There must be one inverse equation for '
                                 'each parameter in this space.')
        obj = BaseSpace.__new__(cls, coords, params, parent_space, implicit,
                                inverse, **kwargs)
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
    def implicit(self):
        return self.args[3]
    @property
    def inverse(self):
        return self.args[4]

    @property
    def order(self):
        """The dimensionality of this subspace."""
        return len(self.params)

    def contains(self, other):
        """Determine if another subspace lies entirely within this subspace.

        Returns
        =======
        A SymPy Boolean object.
        This will indicate how Symbols need to be constrained in order for
        the other subspace to be entirely within this subspace.  This will
        reduce to True or False whenever those Symbols can be more thoroughly
        constrained.

        """
        # If this space is an ancestor of the other, the other subspace will
        # definitely be in this subspace.
        if other.is_descendant(self):
            return True
        self_top = self.in_ancestor()
        other_top = other.in_ancestor()
        # If other has nonzero higher-dimensional coordinates that this
        # subspace does not, other is definitely not in self.
        if len(self_top.coords) < len(other_top.coords) and any(
                c != S.Zero for c in other_top.coords[len(self_top.coords):]):
            return False
        # If self has no parameters, it is a point which can be checked quite
        # easily.
        if self_top.order == 0:
            return And(*(Equality(a,b) for a,b in zip_longest(
                self_top.coords, other_top.coords, fillvalue=0)))
        # If it's not one of the trivial cases, use implicit to check.
        if self.implicit is not None:
            imp = self_top.implicit
            # Replace all global coords in implicit with corresponding coord
            # functions from other.
            for gl, c in zip_longest(global_space, other_top.coords, fillvalue=0):
                # If we have a definitive boolean, we're done.
                if isinstance(imp, bool):
                    return imp
                # Could be any number of global coords in implicit; replace
                # them all until none are left.
                if not any(i.name.startswith("Global") for i in imp.free_symbols):
                    break
                imp = imp.replace(gl, c)
            # If other's parameters appear in imp at this point, it implies
            # that other intersects with self rather than being contained.
            if any(imp.has(i) for i in other.params):
                return False
            return imp
        # If we haven't solved it by now, give up.
        raise NotImplementedError('Implicit definition is required in '
                                  'order to handle non-trivial cases.')

    def _eval_subs(self, old, new):
        """Create new subspace by substituting symbols in coordinate functions.

        """
        new_coords = self.coords.subs(old, new)
        new_parent = self.parent_space.subs(old, new)
        new_implicit = self.implicit.subs(old, new) if (
            self.implicit is not None) else None
        new_inverse = self.inverse.subs(old, new) if (
            self.inverse is not None) else None
        return Subspace(new_coords, self.params, new_parent, new_implicit,
                        new_inverse)

    def in_ancestor(self, n=S.Infinity):
        """Create equivalent subspace in the coordinates of the nth ancestor.

        The zeroth ancestor is this space's parent, so space.is_ancestor(0)
        will always be equal to space.  If n is sufficiently large, a new
        subspace will be returned as a child of global_space.

        """
        p = self.parent_space
        if n == S.Zero or p == global_space:
            return self
        new_coords = p.coords.subs(
            zip_longest(p.params, self.coords, fillvalue=0))
        # Both self's and parent's implicit definitions apply to the new space.
        new_implicit = And(p.implicit, self.implicit) if (
            self.implicit is not None) else None
        # new_implicit may have already evaluated to True or False.  If not,
        # substitute symbols to bring new_implicit into the grandparent space.
        if new_implicit is not None and not isinstance(new_implicit, bool):
            new_implicit = new_implicit.subs(zip(p.params, p.inverse))
        new_inverse = self.inverse.subs(zip(p.params, p.inverse)
            ) if self.inverse is not None else None
        new_space = Subspace(new_coords, self.params, p.parent_space,
                             new_implicit, new_inverse)
        return new_space.in_ancestor(n-1)
