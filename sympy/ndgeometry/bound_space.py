from __future__ import print_function, division

from sympy.ndgeometry.base_space import BaseSpace

class BoundSpace(BaseSpace):
    """Bounded subspace.

    """

    def __new__(cls, parent_space, bounding_loop, **kwargs):
        obj = BaseSpace.__new__(parent_space, bounding_loop, **kwargs)
        obj.parent_space = parent_space
        obj.bounding_loop = bounding_loop
        return obj
