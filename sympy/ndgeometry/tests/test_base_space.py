from sympy import symbols, sin, cos, pi, Equality, Not

from sympy.ndgeometry.subspace import Subspace
from sympy.ndgeometry.global_space import global_space as gl


a, b, c, r, t, x, y, z = symbols('a b c r t x y z')


def test_is_descendant():
    cylinder = Subspace([r*cos(t), r*sin(t), z], [r, t, z])
    circle = Subspace([1, a*2*pi, 3], [a], cylinder)
    point1 = Subspace([0.25], [], circle)
    point2 = Subspace([0, 0, 0], [])
    assert point1.is_descendant(point1)
    assert point1.is_descendant(circle)
    assert circle.is_descendant(cylinder)
    assert point1.is_descendant(cylinder)
    assert not point2.is_descendant(circle)
    assert point1.is_descendant(gl)
    assert point2.is_descendant(gl)
