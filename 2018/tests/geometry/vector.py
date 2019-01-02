import math

import pytest

from geometry import Vector


def EQ():
    assert Vector(1,1) == Vector(1,1)
    assert Vector(1,-2) == Vector(1,-2)
    assert Vector(0,0) == Vector(0,0)

def NE():
    assert Vector(1,1) != Vector(1,2)
    assert Vector(1,1) != Vector(2,1)
    assert Vector(1,1) != Vector(2,2)

def LT():
    assert Vector(1,1) < Vector(1,2)
    assert Vector(1,1) < Vector(2,1)
    assert Vector(1,1) < Vector(2,2)
    assert Vector(1,2) < Vector(2,1)

def GT():
    assert Vector(3,3) > Vector(1,2)
    assert Vector(3,3) > Vector(2,1)
    assert Vector(3,3) > Vector(2,2)
    assert Vector(2,1) > Vector(1,2)

def LE():
    assert Vector(1,1) <= Vector(1,1)
    assert Vector(1,1) <= Vector(1,2)
    assert Vector(1,1) <= Vector(2,1)
    assert Vector(1,1) <= Vector(2,2)
    assert Vector(1,2) <= Vector(2,1)

def GE():
    assert Vector(3,3) >= Vector(3,3)
    assert Vector(3,3) >= Vector(1,2)
    assert Vector(3,3) >= Vector(2,1)
    assert Vector(3,3) >= Vector(2,2)
    assert Vector(2,1) >= Vector(1,2)

def ADD():
    assert Vector(1,1) + Vector(1,1) == Vector(2,2)
    assert Vector(1,1) + Vector(-1,-1) == Vector(0,0)
    assert Vector(1,1) + Vector(0,0) == Vector(1,1)

def SUB():
    assert Vector(1,1) - Vector(1,1) == Vector(0,0)
    assert Vector(2,2) - Vector(1,1) == Vector(1,1)
    assert Vector(0,0) - Vector(1,1) == Vector(-1,-1)

def RMUL():
    assert 4 * Vector(1,2) == Vector(4,8)
    assert 2.2 * Vector(1,2) == Vector(2.2, 4.4)

def normalized():
    assert Vector(1,1).normalized == Vector(1,1)
    assert Vector(1,2).normalized == Vector(0.5,1)
    assert Vector(4,2).normalized == Vector(1,0.5)

def clockwise():
    assert Vector(1,1).clockwise == Vector(1,-1)
    assert Vector(2,1).clockwise == Vector(1,-2)
    assert Vector(-2,1).clockwise == Vector(1,2)

def counterclockwise():
    assert Vector(1,1).counterclockwise == Vector(-1,1)
    assert Vector(2,1).counterclockwise == Vector(-1,2)
    assert Vector(-2,1).counterclockwise == Vector(-1,-2)

def reverse():
    assert Vector(1,1).reverse == Vector(-1,-1)
    assert Vector(2,1).reverse == Vector(-2,-1)
    assert Vector(-2,1).reverse == Vector(2,-1)

def magnitude():
    assert Vector(1,1).magnitude == 2**0.5
    assert Vector(3,4).magnitude == 5
    assert Vector(-3,4).magnitude == 5
    assert Vector(-3,-4).magnitude == 5

def rect_magnitude():
    assert Vector(1,1).rect_magnitude == 2
    assert Vector(3,4).rect_magnitude == 7
    assert Vector(-3,4).rect_magnitude == 7
    assert Vector(-3,-4).rect_magnitude == 7

def dot_product():
    assert Vector(1,1).dot_product(Vector(1,1)) == 2
    assert Vector(2,2).dot_product(Vector(1,1)) == 4
    assert Vector(-2,-2).dot_product(Vector(1,1)) == -4
    assert Vector(-2,2).dot_product(Vector(1,1)) == 0
    assert Vector(2,2).dot_product(Vector(4,4)) == 16
    assert Vector(2.2,2.2).dot_product(Vector(2,2)) == 8.8

def angle_between():
    iota = 1e-06
    
    assert abs(Vector(1,1).angle_between(Vector(1,1))) < iota
    assert abs(Vector(1,1).angle_between(Vector(1,-1)) - math.pi / 2) < iota
    assert abs(Vector(1,1).angle_between(Vector(-1,-1)) - math.pi) < iota

def copy():
    fixture = Vector(1,1)
    
    assert fixture == fixture.copy()
    assert fixture is not fixture.copy()
