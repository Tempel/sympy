from __future__ import print_function, division

from sympy import symbols, oo
from sympy.utilities.pytest import raises

from sympy.ndgeometry.global_space import GlobalSpace, global_space


def test_equality():
    assert global_space == GlobalSpace()
    assert GlobalSpace() == GlobalSpace()


def test_getitem():
    assert global_space[2] == symbols('Global2')
    raises(ValueError, lambda: global_space['a'])
    assert global_space[1:3] == symbols('Global1 Global2')
    assert global_space.x == symbols('Global0')
    assert global_space.y == symbols('Global1')
    assert global_space.z == symbols('Global2')


def test_iter():
    for i, s in enumerate(global_space):
        assert s == symbols('Global{0}'.format(i))
        if i > 150:
            break
