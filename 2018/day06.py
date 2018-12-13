from functools import reduce
from itertools import permutations, count
import math
import operator as op
import re

from geometry import Grid as GridBase, Point as PointBase


def load(input_filename):
    with open(input_filename, 'r') as f:
        pattern = re.compile(r'(?P<x>\d+), (?P<y>\d+)')
        
        for line in f:
            match = pattern.match(line.strip())
            
            yield Point(int(match.group('x')), int(match.group('y')))

def common_part(data=None, test=False):
    data = data or (test and load('input/6.test')) or load('input/6')
    
    grid = Grid(data)
    
    return grid

def part1(data=None, test=False):
    return common_part(data, test)

def part2(distance_threshold, data=None, test=False):
    grid = common_part(data, test)
    
    minx = min(x.x for x in grid.points) - distance_threshold
    miny = min(x.y for x in grid.points) - distance_threshold
    maxx = max(x.x for x in grid.points) + distance_threshold
    maxy = max(x.y for x in grid.points) + distance_threshold
    
    for x,y in ((x,y) for x in range(minx, maxx+1) for y in range(miny, maxy+1)):
        candidate = Point(x,y)
        total_distance = 0
        
        #summing manually so as to shortcut if the threshold is passed
        for point in grid.points:
            total_distance += candidate.distance_to(point)
            if total_distance >= distance_threshold:
                total_distance = None
                break
        
        if total_distance and total_distance < distance_threshold:
            yield (x,y), total_distance
    
    ### NOTE: yielded 47841 qualifying points in about 10 minutes


class Grid(GridBase):
    
    @property
    def points_with_finite_areas(self):
        return [x for x in self.points if x.smooth_area.is_bounded]

class Point(PointBase):
    
    @property
    def smooth_area(self):
        return reduce(op.and_, (Area.split_plane(LineSegment(self, x).bisection, self) for x in self.grid.points if x != self))
    
    @property
    def manhattan_area(self):
        #extend outward in concentric rings (diamonds), testing the distance to every point
        #once a full ring has been done without finding one closest to me, stop
        
        for distance in count(0):
            found_any = False
            
            for candidate in self.points_at_distance(distance):
                if all(distance < candidate.distance_to(x) for x in self.grid.points if x != self):
                    found_any = True
                    yield candidate
            
            if not found_any:
                break
