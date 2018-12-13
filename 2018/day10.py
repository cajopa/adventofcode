#!/usr/bin/env python

from itertools import product
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
    
    return str(common_part(data=data).convergent_future)

def part2(data=None):
    ''


class Grid(GridBase):
    def __str__(self):
        return '\n'.join(''.join(str(self[x,y]) for x in self.x_range) for y in self.y_range)
    
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except (StopIteration, LookupError):
            return NullPoint(*key)
    
    def __contains__(self, key):
        if isinstance(key, tuple):
            return any(1 for x in self.dots if (x.x, x.y) == key)
        if isinstance(key, Point):
            return any(1 for x in self.dots if x.position == key)
        else:
            return NotImplemented
    
    @property
    def dots(self):
        return self.points
    
    @dots.setter
    def dots(self, value):
        self.points = value
    
    @property
    def x_range(self):
        minx = int(min(x.x for x in self.dots))
        maxx = int(max(x.x for x in self.dots))
        
        return range(minx, maxx + 1)
    
    @property
    def y_range(self):
        miny = int(min(x.y for x in self.dots))
        maxy = int(max(x.y for x in self.dots))
        
        return range(miny, maxy + 1)
    
    @property
    def cohesion(self):
        '''
        ratio of points that touch other points, including diagonal
        
        orthogonal neighbors weighted double
        '''
        
        return sum(x.neighbor_score for x in self.dots) / len(self.dots)
    
    @property
    def convergent_future(self):
        '''
        find the most cohesive future self
        
        cohesion is not guaranteed to be monotonic over time - build in some overshoot
        '''
        
        max_cohesion = 0
        best_future = None
        overshoot = 10
        
        for i,future_grid in enumerate(self.iterate()):
            cohesion = future_grid.cohesion
            
            if cohesion > max_cohesion:
                print('o', end='', flush=True)
                max_cohesion = cohesion
                best_future = future_grid
                overshoot = 10
            elif cohesion < max_cohesion:
                print('-', end='', flush=True)
                if overshoot:
                    overshoot -= 1
                else:
                    return best_future
            else:
                print('.', end='', flush=True)
    
    def iterate(self, direction=1):
        current = self
        
        while True:
            current = current.increment(direction/abs(direction))
            
            yield current
    
    def increment(self, amount=1):
        to_return = self.copy()
        
        for dot in to_return.dots:
            dot.increment(amount)
        
        return to_return
    
    def copy(self):
        return self.__class__(x.copy() for x in self.dots)

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
    
    def __repr__(self):
        return f'<{self.__class__.__name__} ({self.position.x}, {self.position.y}) -> [{self.velocity.x}, {self.velocity.y}]>'
    
    def __str__(self):
        return str(self.position)
    
    @classmethod
    def from_raw(cls, px, py, vx, vy):
        return cls(Point(int(px), int(py)), Vector(int(vx), int(vy)))
    
    @property
    def has_neighbor(self):
        return self.has_orthogonal_neighbor or self.has_diagonal_neighbor
    
    @property
    def has_diagonal_neighbor(self):
        neighbor_offsets = [(-1,-1), (-1,1), (1,-1), (1,1)]
        
        return any((Point(*x) + self.position) in self.grid for x in neighbor_offsets)
    
    @property
    def has_orthogonal_neighbor(self):
        neighbor_offsets = [(-1,0), (1,0), (0,-1), (0,1)]
        
        return any((Point(*x) + self.position) in self.grid for x in neighbor_offsets)
    
    @property
    def neighbor_score(self):
        if self.has_orthogonal_neighbor:
            return 1
        elif self.has_diagonal_neighbor:
            return 0.5
        else:
            return 0
    
    @property
    def x(self):
        return self.position.x
    
    @property
    def y(self):
        return self.position.y
    
    def increment(self, amount=1):
        self.position += amount * self.velocity
    
    def copy(self):
        return self.__class__(self.position.copy(), self.velocity.copy())


if __name__=='__main__':
    run_as_script(part1, {load('input/10.test'): open('input/10.test.result','r').read().strip()}, part2, {})
