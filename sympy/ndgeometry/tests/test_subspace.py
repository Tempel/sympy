from sympy import symbols, sin, cos, pi, sqrt, Equality, Not

from sympy.ndgeometry.subspace import Subspace
from sympy.ndgeometry.global_space import global_space as gl


a, b, c, r, t, x, y, z = symbols('a b c r t x y z')


def test_parameters():
    # Symbols that are not parameters.
    point = Subspace([a, b, c], [])
    assert point.order == 0
    assert point.subs({a:1, b:2, c:3}).order == 0
    # Symbols as parameters; substitution does not affect parameter list.
    curve = Subspace([2*x, x**2-1], [x])
    assert curve.subs(x, 4) == Subspace([8, 15], [x])
    surface = Subspace([x, y, sin(x*y)], [x, y])
    assert surface.subs(x, 4) == Subspace([4, y, sin(4*y)], [x, y])
    # Symbols in parent space.
    curve2 = Subspace([a*x, x**a-b], [x])
    point2 = Subspace([4], [], curve2)
    assert point2.subs(a, 3) == Subspace([4], [], Subspace([3*x, x**3-b], [x]))
    assert point2.subs(x, 1) == Subspace([4], [], Subspace([a, 1-b], [x]))


def test_parents():
    # Alternate parent space and conversion to grandparent's coordinate space.
    cylinder = Subspace([r*cos(t), r*sin(t), z], [r, t, z])
    circle = Subspace([1, a*2*pi, 3], [a], cylinder)
    point = Subspace([0.25], [], circle)
    assert point.in_ancestor(0) == point
    assert point.in_ancestor(1) == Subspace([1, pi/2, 3], [], cylinder)
    assert point.in_ancestor(2) == Subspace([0, 1, 3], [])
    assert point.in_ancestor() == point.in_ancestor(2)
    # Fewer coordinates than parent space parameters.
    point2 = Subspace([2, pi/4], [], cylinder)
    assert point2.in_ancestor() == Subspace([sqrt(2), sqrt(2), 0], [])


def test_contains():
    # When in parent/grandparent space.
    cylinder = Subspace([r*cos(t), r*sin(t), z], [r, t, z])
    circle = Subspace([1, a*2*pi, 3], [a], cylinder)
    point1 = Subspace([0.25], [], circle)
    point2 = Subspace([0, 0, 0], [])
    assert point1 in point1
    assert point1 in circle
    assert circle in cylinder
    assert point1 in cylinder
    assert point2 not in circle
    # When in other space.
    circle2 = ([cos(t), sin(t), 3], [t])
    point3 = Subspace([1, 0, 3], [])
    assert point3 in circle
    assert point2 in cylinder
    assert circle2 in circle
    # When including symbols.
    point4 = Subspace([0, 1, b], [])
    assert (point4 in circle) == Equality(b, 3)
    assert (point4 not in circle) == Not(Equality(b, 3))
    assert point4 in cylinder
