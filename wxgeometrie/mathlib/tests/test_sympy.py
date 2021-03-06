# -*- coding: utf-8 -*-
from __future__ import division # 1/2 == .5 (par defaut, 1/2 == 0)

import os, math

from pytest import XFAIL

from sympy import (Symbol, exp, solve, limit, S, E, Matrix, Integer, oo,
                    sympify, Float, sqrt,
                    )

from tools.testlib import assertAlmostEqual, assertEqual

# Teste que certains bugs de sympy sont bien ou résolus, ou temporairement patchés



def test_sympy():
    x = Symbol('x', real=True)
    assert -oo < oo
    assert not(-1.5 < -oo)
    assert (1 - exp(x)).is_negative is None
    assert Matrix([[1, 2], [3, 4]])**Integer(2) == Matrix([[7, 10], [15, 22]])
    assertAlmostEqual(E._evalf(50), math.e)
    assert solve(1/x, x) == [] # issue 1694
    assert solve(-(1 + x)/(2 + x)**2 + 1/(2 + x), x) == [] # issue 1694
    assert limit(1 + 1/x, x, 0, dir='-') == -oo
    assert limit(1/x**2, x, 0, dir='-') == oo
    assert sympify(u'45') == 45 # issue 2508
    assertEqual(solve((2*x + 8)*exp(-6*x), x), [-4]) # issue 10391 (FS#319)


def test_sympy_solving_with_floats():
    x = Symbol('x', real=True)

    sols = solve(exp(-Float('0.5')*x + Float('0.4')) - 1)
    assert len(sols) == 1
    sol = sols[0]
    assertAlmostEqual(sol, Float('0.8'))

    sols = solve(exp(-Float('0.5')*x - Float('0.4')) - 1)
    assert len(sols) == 1
    sol = sols[0]
    assertAlmostEqual(sol, Float('-0.8'))

    sols = solve(exp(-Float('0.5', 10)*x + Float('0.4', 10)) - 1)
    assert len(sols) == 1
    sol = sols[0]
    assertAlmostEqual(sol, Float('0.8'))

def test_sympy_1_div_0():
    assert S.One/S.Zero is S.ComplexInfinity

def test_sympy_files():
    sympy_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + '/../../sympy')
    def tst(path):
        assert os.path.isfile(os.path.join(sympy_dir, path))
    tst('AUTHORS')
    tst('LICENSE')
    tst('README.rst')



def test_solve_reals():
    x = Symbol('x', real=True)
    assert solve(sqrt(x)) == [0]

def test_set():
    assert S(2) == 2
    assert {S(2)} == {2}
