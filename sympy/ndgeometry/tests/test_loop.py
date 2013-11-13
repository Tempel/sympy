from __future__ import print_function, division

from sympy import symbols, Equality as Eq
from sympy.utilities.pytest import raises

from sympy.ndgeometry.bound_space import BoundSpace
from sympy.ndgeometry.loop import Loop
from sympy.ndgeometry.subspace import Subspace


a, b, c, r, t, x, y, z = symbols('a b c r t x y z')


def test_creation_points():
    p1 = Subspace((1, 2, 3), [])
    p2 = Subspace((3, 4, 5), [])
    l = Loop([p1, p2])
    assert l.order == 0
    # Wrong number of points.
    raises(ValueError, lambda: Loop([p1]))
    p3 = Subspace((a, b, c), [])
    raises(ValueError, lambda: Loop([p1, p2, p3]))

def test_creation():
    pass
    # TODO Inconsistent order.
    # TODO Non-manifold.
