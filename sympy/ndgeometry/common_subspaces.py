from __future__ import print_function, division

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

from sympy import symbols, pi, sin, cos, atan2, sqrt, Dummy
from sympy.core.containers import Tuple
from sympy.core.relational import Equality
from sympy.logic.boolalg import And
from sympy.matrices import Matrix, eye

from sympy.ndgeometry.base_space import BaseSpace
from sympy.ndgeometry.subspace import Subspace
from sympy.ndgeometry.global_space import global_space as gl


# Transforming spaces.

class Cylindrical(Subspace):

    def __new__(cls, parent_space=gl, **kwargs):
        # Dummy symbol needed for inverse; use one dummy for each instance.
        # TODO Do we want consistent dummies?
        dummy = symbols('n', integer=True, cls=Dummy)
        return BaseSpace.__new__(cls, parent_space, dummy, **kwargs)
    @property
    def dummy(self):
        return self.args[1]
    n = dummy

    @property
    def coords(self):
        r, theta, z = self.params
        return Tuple(r*cos(theta), r*sin(theta), z)
    @property
    def params(self):
        return Tuple(*symbols('r theta z'))
    @property
    def parent_space(self):
        return self.args[0]
    @property
    def implicit(self):
        return True
    @property
    def inverse(self):
        x, y, z = self.parent_space.params[0:3]
        return Tuple(sqrt(x**2+y**2), atan2(y, x) + 2*pi*self.n, z)


class Spherical(Subspace):

    def __new__(cls, parent_space=gl):
        return BaseSpace.__new__(cls, parent_space, **kwargs)

    @property
    def coords(self):
        r, theta, phi = self.params
        # TODO
    def params(self):
        return Tuple(*symbols('r theta phi'))
    @property
    def parent_space(self):
        return self.args[0]
    @property
    def implicit(self):
        return True
    @property
    def inverse(self):
        n = symbols('n', integer=True)
        # TODO


class Translate(Subspace):
    pass # TODO


class Rotate(Subspace):
    pass # TODO


class RigidTransform(Subspace):
    pass # TODO


# Arbitrary-order subspaces.

class VectorSpace(Subspace):

    def __new__(cls, start, vectors, parent_space=gl, **kwargs):
        # Allow start to be tuple or zero-order subspace.
        if isinstance(start, Subspace):
            if start.order != 0:
                raise TypeError('Start must be a point (i.e. order zero).')
            start = start.coords
        # If start and vectors don't have the same dimensionality, fill any
        # leftover dimensions with zeros.
        start = list(start)
        vectors = [list(v) for v in vectors]
        max_dim = len(start)
        for v in vectors:
            l = len(v)
            if l > max_dim:
                max_dim = l
        start.extend([0] * (max_dim - len(start)))
        for v in vectors:
            v.extend([0] * (max_dim - len(v)))
        # Convert start point and all vectors to Tuples.
        start = Tuple(*start)
        vectors = Tuple(*(Tuple(*v) for v in vectors))
        return BaseSpace.__new__(cls, start, vectors, parent_space, **kwargs)

    @property
    def start(self):
        return self.args[0]
    @property
    def vectors(self):
        return self.args[1]

    @property
    def coords(self):
        p_vectors = []
        for p, vec in zip(self.params, self.vectors):
            p_vectors.append([p*v for v in vec])
        return Tuple(*(sum(i) for i in zip(self.start, *p_vectors)))
    @property
    def params(self):
        return Tuple(*symbols('t:{0}'.format(len(self.vectors))))
    @property
    def parent_space(self):
        return self.args[2]

    @property
    def implicit(self):
        # The Moore-Penrose pseudoinverse produces exact results if available,
        # and approximate results otherwise.  Check if the results produce the
        # original subspace coordinates to determine if the results are exact.
        A = Matrix(self.vectors).T
        b1 = Matrix(self.parent_space.params[:len(self.start)])
        b2 = Matrix(self.start)
        B = b1 - b2
        return Equality(A * A.pinv() * B, B)

    @property
    def inverse(self):
        # Employ the Moore-Penrose pseudoinverse to find approximate solutions.
        # Check with implicit to see if approximate solutions satisfy the
        # equation.
        A = Matrix(self.vectors).T
        b1 = Matrix(self.parent_space.params[:len(self.start)])
        b2 = Matrix(self.start)
        B = b1 - b2
        # TODO Somehow get consistent dummies, maybe?
        # TODO Do we really want consistent dummies?
        return Tuple(*A.pinv_solve(B))

    @classmethod
    def through_points(cls, points, parent_space=gl):
        start = points[0]
        vectors = [ [b-a for a,b in zip_longest(start, p, fillvalue=0)]
                    for p in points[1:] ]
        return cls(start, vectors, parent_space)


# Common first-order spaces (curves).

Line = VectorSpace
# TODO Subclass VectorSpace to restrict number of inputs for Line?

class Circle(Subspace):
    # TODO
    @classmethod
    def through_points(cls, p1, p2, p3, parent_space=gl):
        pass # TODO


class Ellipse(Subspace):
    pass # TODO


class Spline(Subspace):
    pass # TODO


# Common second-order spaces (surfaces).

Plane = VectorSpace
# TODO Subclass VectorSpace to restrict number of inputs for Plane?
