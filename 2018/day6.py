import re


def load(input_filename):
    with open(input_filename, 'r') as f:
        pattern = re.compile(r'(?P<x>\d+), (?P<y>\d+)')
        
        for line in f:
            match = pattern.match(line.strip())
            
            yield Point(int(match.group('x')), int(match.group('y')))

def part1(data=None, test=False, debug=False):
    data = data or (test and load('input/6.test')) or load('input/6')
    
    grid = Grid(data)
    
    return grid

def part2(data=None, debug=False):
    pass


class Point:
    def __init__(self, x, y):
        self.grid = None
        
        self.x = x
        self.y = y
    
    @property
    def has_finite_area(self):
        #is the area bounded by the bisections of the lines between this and every other point entirely convex?
        
        pass
    
    def distance_to(self, other):
        return (self.x - other.x) + (self.y - other.y)

class LineSegment:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    @property
    def as_vector(self):
        return Vector(self.start.x - self.end.x, self.start.y - self.end.y)
    
    @property
    def bisection(self):
        midpoint = Point((self.start.x + self.end.x)/2, (self.start.y + self.end.y)/2)
        
        return Line(midpoint, self.as_vector.clockwise)

class Line:
    def __init__(self, start, vector):
        self.start = start
        self.vector = vector
    
    def _determinant(self, line):
        return self.vector.y*line.vector.x - self.vector.x*line.vector.y
    
    def intersects(self, other):
        if isinstance(other, Line):
            if type(other) is Line:
                return self._determinant(other) != 0
            else:
                return other.intersects(self)
        else:
            raise ValueError('other must be a line')
    
    def congruent_with(self, other):
        return (
            isinstance(other, Line)
            and self.vector == other.vector
            and (self.start.x - other.start.x) / self.vector.x == (self.start.y - other.start.y) / self.vector.y
        )

class Ray(Line):
    def intersects(self, line):
        determinant = self._determinant(line)
        
        if determinant:
            tr = (line.vector.x*(line.start.y - self.start.y) - line.vector.y*(line.start.x - self.start.x)) / determinant
            
            return determinant and tr >= 0
        else:
            return False

class Edge:
    def __init__(self, line, normal):
        self.line = line
        self.normal = normal

class Area:
    def __init__(self, edges):
        self.edges = list(edges)
    
    @classmethod
    def split_plane(cls, line, point):
        left_side = cls([Edge(line, Vector(-1,0))])
        right_side = cls([Edge(line, Vector(1,0))])
        
        if point in left_side:
            return left_side
        else:
            return right_side
    
    def __contains__(self, point):
        if len(self.edges) == 1:
            return Ray(point, self.edges[0].normal.reverse).intersects(self.edges[0].line)
        else:
            return all((point in x) for x in self.decomposition)
    
    def intersection(self, other):
        return self.__class__(self.edges + other.edges)
    
    def intersection_update(self, other):
        self.edges.extend(other.edges)
    
    @property
    def is_bounded(self):
        #do all edges intersect at least two distinct others?
        pass
    
    @property
    def decomposition(self):
        return (self.__class__([x]) for x in self.edges)

class Vector:
    def __init__(self, x, y):
        #normalize to the unit square
        divisor = max(map(abs, [x, y]))
        
        self.x = x / divisor
        self.y = y / divisor
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    @property
    def clockwise(self):
        return self.__class__(self.y, -self.x)
    
    @property
    def counterclockwise(self):
        return self.__class__(-self.y, self.x)
    
    @property
    def reverse(self):
        return self.__class__(-self.x, -self.y)

class Grid:
    def __init__(self, points):
        self.points = tuple(points)
        
        for point in points:
            point.grid = self
