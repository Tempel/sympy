from sympy import symbols, sin, cos, pi
from sympy.ndgeometry.subspace import Subspace

a, b, c, r, t, x, y, z = symbols('a b c r t x y z')

def test_parameters():
    # Symbols that are not parameters.
    point = Subspace([a, b, c], [])
    assert point.order == 0
    assert point.subs({a:1, b:2, c:3}).order == 0
    # Symbols as parameters; substitution removes parameter.
    curve = Subspace([2*x, x**2-1], [x])
    assert curve.order == 1
    assert curve.subs({x:4}).order == 0
    surface = Subspace([x, y, sin(x*y)], [x, y])
    assert surface.order == 2
    assert surface.subs({x:4}).order == 1


def test_parents():
    # Alternate parent space and conversion to grandparent's coordinate space.
    cylinder = Subspace([r*cos(t), r*sin(t), z], [r, t, z])
    circle = Subspace([1, a*2*pi, 3], [a], cylinder)
    point = Subspace([0.25], [], circle)
    assert point.in_ancestor(0) == point
    assert point.in_ancestor(1) == Subspace([1, pi/2, 3], [], cylinder)
    assert point.in_ancestor(2) == Subspace([0, 1, 3], [])
    assert point.in_ancestor() == point.in_ancestor(2)
