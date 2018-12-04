from itertools import product
from collections import defaultdict
import re


def load(input_filename):
    pattern = re.compile(r'^#(?P<id>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)$')
    
    with open(input_filename, 'r') as f:
        for line in f:
            match = pattern.match(line.strip())
            
            yield (
                int(match.group('id')),
                int(match.group('left')),
                int(match.group('top')),
                int(match.group('width')),
                int(match.group('height')),
            )

def part1():
    data = load('input/3')
    
    grid = defaultdict(lambda: 0)
    
    for id_,left,top,width,height in data:
        for x,y in product(range(left, left+width), range(top, top+height)):
            grid[x,y] += 1
    
    return sum(1 for x in grid.values() if len(x) > 1)

def part2():
    claims = [Claim(x[0], x[1], x[2], x[3], x[4]) for x in load('input/3')]
    
    grid = defaultdict(lambda: set())
    
    for claim in claims:
        for point in claim.points:
            grid[point].add(claim)
    
    nonoverlapping_points = {k:v for k,v in grid.items() if len(v) == 1}
    
    #map claims found for nonoverlapping points to those points
    candidates = defaultdict(set)
    for point, claims in nonoverlapping_points.items():
        for claim in claims:
            candidates[claim].add(point)
    
    #do the non-overlapping points that each ID maps to make up the whole set?
    for claim, points in candidates.items():
        if points == set(claim.points):
            yield claim


class Claim:
    def __init__(self, id_, left, top, width, height):
        self.id_ = id_
        self.left = left
        self.top = top
        self.width = width
        self.height = height
    
    def __str__(self):
        return '<{self.__class__.__name__}: #{self.id_} @ {self.left},{self.top}: {self.width}x{self.height}>'.format(self=self)
    __repr__=__str__
    
    @property
    def points(self):
        yield from product(range(self.left, self.left+self.width), range(self.top, self.top+self.height))
