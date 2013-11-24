from __future__ import print_function, division

from sympy.ndgeometry.base_space import BaseSpace

class BoundSpace(BaseSpace):
    """Bounded subspace.

    """

    def __new__(cls, parent_space, bounding_loop):
        if bounding_loop.order != parent_space.order-1:
            raise ValueError("Bounding loop's order must be one lower than "
                             "parent space's order.")
        return BaseSpace.__new__(cls, parent_space, bounding_loop)
