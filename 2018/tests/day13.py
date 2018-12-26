from day13 import *


def test_part1_full():
    assert part1(load('input/13.1.test')) == Vector(7,3)

def test_part1_mini():
    assert part1(load('input/13.1.test.mini')) == Vector(4,4)

def test_part2():
    assert part2(load('input/13.2.test')) == Vector(6,4)
