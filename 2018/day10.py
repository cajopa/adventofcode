#!/usr/bin/env python

import re

from geometry import Point as PointBase, Vector, Grid as GridBase
from util import run_as_script


def load(input_filename):
    with open(input_filename, 'r') as f:
        #position=< 10387, -40807> velocity=<-1,  4>
        pattern = re.compile(r'position=< *(?P<px>-?\d+), *(?P<py>-?\d+)> velocity=< *(?P<vx>-?\d+), *(?P<vy>-?\d+)>')
        
        for line in f:
            match = pattern.match(line.strip())
            
            if match:
                yield Dot.from_raw(match.group('px'), match.group('py'), match.group('vx'), match.group('vy'))
            else:
                print(f'!!!!! FAILED TO PARSE LINE: {line}')

def common_part(data=None):
    dots = data or load('input/10')
    
    return Grid(dots)

def part1(data=None):
    '''
    What message will eventually appear in the sky?
    '''
    
    ### HELP: how to tell when the message has appeared?

def part2(data=None):
    ''


class Grid(GridBase):
    def __str__(self):
        return '\n'.join(''.join(str(self[x,y]) for x in self.x_range) for y in self.y_range)
    
    def __getitem__(self, key):
        try:
            super().__getitem__(key)
        except (StopIteration, LookupError):
            return NullPoint(*key)
    
    @property
    def dots(self):
        return self.points
    
    @dots.setter
    def dots(self, value):
        self.points = value
    
    @property
    def x_range(self):
        minx = min(x.x for x in self.dots)
        maxx = max(x.x for x in self.dots)
        
        return range(minx, maxx + 1)
    
    @property
    def y_range(self):
        miny = min(x.y for x in self.dots)
        maxy = max(x.y for x in self.dots)
        
        return range(self.miny, self.maxy + 1)

class Point(PointBase):
    def __str__(self):
        return '#'

class NullPoint(PointBase):
    def __str__(self):
        return '.'

class Dot:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        
        self.grid = None
    
    @classmethod
    def from_raw(cls, px, py, vx, vy):
        return cls(Point(int(px), int(py)), Vector(int(vx), int(vy)))


if __name__=='__main__':
    run_as_script(part1, {load('input/10.test'): open('input/10.test.result','r').read().strip()}, part2, {})
