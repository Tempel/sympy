from __future__ import print_function, division

from collections import Counter

from sympy.core.containers import Tuple

from sympy.ndgeometry.base_space import BaseSpace

class Loop(BaseSpace):
    """A loop of bounded subspaces.

    Defined as a set of same-order bound spaces with all of their bounding
    spaces shared by exactly two members of the loop.  A loop need not be a
    single closed loop.  Note that points do not form a loop in the same way;
    a "loop" of points is just two points.

    """

    def __new__(cls, members):
        members = Tuple(*members)
        order = members[0].order
        for m in members[1:]:
            if m.order != order:
                raise ValueError('All members of the loop must be of the same '
                                 'order (i.e. have the same number of '
                                 'parameters).')
        # Treat a "loop" of points specially and skip manifold check.
        if order == 0:
            if len(members) != 2:
                raise ValueError('A loop of points must consist of just two.')
        else:
            # Check that the whole thing is 2-manifold (i.e. bounding spaces
            # are shared by exactly two members).
            bounds = Counter()
            for m in members:
                bounds.update(m.bounding_loop.members)
            if not all(b == 2 for b in bounds.values()):
                raise ValueError('Loop is not 2-manifold: some bounds are '
                                 'shared more or less than twice.')
        return BaseSpace.__new__(cls, members)

    @property
    def members(self):
        return self.args[0]
    @property
    def order(self):
        return self.members[0].order
