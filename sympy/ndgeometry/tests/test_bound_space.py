from __future__ import print_function, division

from sympy import symbols, Equality as Eq
from sympy.utilities.pytest import raises

from sympy.ndgeometry.common_subspaces import VectorSpace
from sympy.ndgeometry.bound_space import BoundSpace
from sympy.ndgeometry.loop import Loop
from sympy.ndgeometry.subspace import Subspace


a, b, c, r, t, x, y, z = symbols('a b c r t x y z')


def test_creation():
    p1 = Subspace((0, 0, 0), [])
    p2 = Subspace((2, 4, 6), [])
    segment = BoundSpace(Subspace((a, 2*a, 3*a), [a]), Loop([p1, p2]))
