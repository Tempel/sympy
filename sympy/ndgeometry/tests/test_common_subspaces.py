from __future__ import print_function, division

from sympy import symbols, pi, sqrt, Equality, Matrix, Dummy
from sympy.utilities.pytest import raises

from sympy.ndgeometry.common_subspaces import Cylindrical, VectorSpace
from sympy.ndgeometry.global_space import global_space as gl
from sympy.ndgeometry.subspace import Subspace


def test_cylindrical():
    c = Cylindrical()
    r, t, z = c.params
    n = c.inverse.atoms(Dummy).pop()
    assert c.coords.subs({r: 1, t: pi/4, z: 1}) == (1/sqrt(2), 1/sqrt(2), 1)
    assert (c.inverse.subs({gl.x: 1/sqrt(2), gl.y: 1/sqrt(2), gl.z: 1}) ==
            (1, 2*n*pi + pi/4, 1))


def test_vectorspace():
    t0, t1, t2 = symbols('t:3')
    # Test basics for first-order vector space.
    line = VectorSpace((0,0), [(1,1)])
    assert line.start == (0,0)
    assert line.vectors == ((1,1),)
    assert line.coords == (t0, t0)
    assert line.params == (t0,)
    assert line.parent_space == gl
    # Ignore specifics of implicit and inverse algorithms.
    assert line.implicit.subs(gl.y, gl.x) is True
    assert line.inverse.subs(gl.y, gl.x) == (gl.x,)
    assert line.contains(Subspace((7, 7), []))
    # TODO Equalities of unequal matrices do not simplify down.
    #assert not line.contains(Subpace((8, 7), []))
    plane = VectorSpace((1,), [(1,1), (0,1,1)])
    assert plane.start == (1,0,0)
    assert plane.vectors == ((1,1,0),(0,1,1))
    assert plane.coords == (1 + t0, t0 + t1, t1)
    assert plane.params == (t0, t1)
    assert plane.implicit.subs(gl.y, gl.x-1+gl.z) is True
    assert plane.inverse.subs(gl.y, gl.x-1+gl.z) == (gl.x-1, gl.z)
    # Test creation through a set of points.
    assert (VectorSpace.through_points([(0,0), (1,1)]) ==
            VectorSpace((0,0), [(1,1)]))
    assert (VectorSpace.through_points([(0,0), (1,1), (0,1,1)]) ==
            VectorSpace((0,0,0), [(1,1,0), (0,1,1)]))
    assert (VectorSpace.through_points([(-1,0), (1,1), (0,1,1)]) ==
            VectorSpace((-1,0,0), [(2,1,0), (1,1,1)]))
    # Test errors on invalid values.
    # Start is not a point.
    raises(TypeError, lambda: VectorSpace(1, [(1,1)]))
    raises(TypeError, lambda: VectorSpace(Cylindrical(), [(1,1)]))
    # Vectors is not a list of vectors.
    raises(TypeError, lambda: VectorSpace((0,0), (1,1)))
    # Test spaces with redundant vectors: they must be supported.
    splane = VectorSpace((0,), [(0,), (1,0), (0,1)])
    assert splane.start == (0,0)
    assert splane.vectors == ((0,0), (1,0), (0,1))
    assert splane.coords == (t1, t2)
    assert splane.params == (t0, t1, t2)
    assert splane.implicit == True
    inv = splane.inverse
    w0 = inv.atoms(Dummy).pop()
    assert inv == (w0, gl.x, gl.y)
    splane2 = VectorSpace((0,), [(1,), (1,1), (0,1)])
    assert splane2.start == (0,0)
    assert splane2.vectors == ((1,0), (1,1), (0,1))
    assert splane2.coords == (t0 + t1, t1 + t2)
    assert splane2.params == (t0, t1, t2)
    assert splane2.implicit == True
    # TODO This test is difficult for me to figure out.
    #inv = splane2.inverse
    #w0 = inv.atoms(Dummy).pop()
    #assert inv == (gl.x - w0, w0, gl.y - w0)
