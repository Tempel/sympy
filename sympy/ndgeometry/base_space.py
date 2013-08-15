from __future__ import print_function, division

from sympy.core.basic import Basic

class BaseSpace(Basic):

    def is_descendant(self, other):
        """Determine if another subspace is ((great)grand)parent to this.

        Returns
        =======
        bool

        """
        if self is other or self.parent_space.is_descendant(other):
            return True
