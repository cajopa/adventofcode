from numbers import Number


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'<Vector ({self.x},{self.y})>'
    __str__=__repr__
    
    def __eq__(self, other):
        return isinstance(other, Vector) and tuple(self) == tuple(other)
    
    def __lt__(self, other):
        return isinstance(other, Vector) and tuple(self) < tuple(other)
    
    def __gt__(self, other):
        return isinstance(other, Vector) and tuple(self) > tuple(other)
    
    def __le__(self, other):
        return self == other or self < other
    
    def __ge__(self, other):
        return self == other or self > other
    
    def __ne__(self, other):
        return not self == other
    
    def __hash__(self):
        return hash(self.__class__) ^ hash((self.x, self.y))
    
    def __add__(self, other):
        if not isinstance(other, Vector):
            raise ValueError('other must be a Vector')
        
        return self.__class__(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return self + -1 * other
    
    def __rmul__(self, other):
        if isinstance(other, Number):
            return self.__class__(self.x * other, self.y * other)
        else:
            return NotImplemented
    
    def __iter__(self):
        yield self.x
        yield self.y
    
    @property
    def normalized(self):
        divisor = max([self.x, self.y], key=abs)
        
        return self.__class__(self.x / divisor, self.y / divisor)
    
    @property
    def clockwise(self):
        return self.__class__(self.y, -self.x)
    
    @property
    def counterclockwise(self):
        return self.__class__(-self.y, self.x)
    
    @property
    def reverse(self):
        return self.__class__(-self.x, -self.y)
    
    @property
    def magnitude(self):
        return (self.x**2 + self.y**2) ** 0.5
    
    def dot_product(self, other):
        return self.x * other.x + self.y * other.y
    
    def angle_between(self, other):
        return math.acos(self.dot_product(other) / self.magnitude / other.magnitude)
    
    def copy(self):
        return self.__class__(self.x, self.y)

class Point(Vector):
    def __init__(self, x, y, name=None):
        super().__init__(x, y)
        
        self.grid = None
        
        self.name = name
    
    def __repr__(self):
        if self.name:
            return f'<Point {self.name}>'
        else:
            return f'<Point x:{self.x} y:{self.y}>'
    __str__=__repr__
    
    def points_at_distance(self, distance):
        for x in range(-distance, distance+1):
            if abs(x) == distance:
                yield self.__class__(self.x + x, self.y)
            else:
                y_magnitude = distance - abs(x)
                
                yield self.__class__(self.x + x, self.y + y_magnitude)
                yield self.__class__(self.x + x, self.y - y_magnitude)
    
    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def copy(self):
        return self.__class__(self.x, self.y, name=self.name)

class LineSegment:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f'<LineSegment start:{self.start} end:{self.end}>'
    __str__=__repr__
    
    @property
    def as_vector(self):
        return Vector(self.start.x - self.end.x, self.start.y - self.end.y)
    
    @property
    def bisection(self):
        midpoint = Point((self.start.x + self.end.x)/2, (self.start.y + self.end.y)/2)
        
        return Line(midpoint, self.as_vector.clockwise.normalized)

class Line:
    def __init__(self, start, vector):
        self.start = start
        self.vector = vector
    
    def __repr__(self):
        return f'<Line start:{self.start} vector:{self.vector}>'
    __str__=__repr__
    
    def __contains__(self, point):
        return self.vector.y * (point.x - self.start.x) == self.vector.x * (point.y - self.start.y)
    
    def __and__(self, other):
        return self.intersection(other)
    
    def determinant(self, line):
        return self.vector.y*line.vector.x - self.vector.x*line.vector.y
    
    def intersects(self, other):
        if isinstance(other, Line):
            if type(other) is Line:
                return self.determinant(other) != 0
            else:
                return other.intersects(self)
        else:
            raise ValueError('other must be a Line')
    
    def intersection(self, other):
        u = (other.vector.x * (other.start.y - self.start.y) - other.vector.y * (other.start.x - self.start.x)) / self.determinant(other)
        
        return Point(self.start.x + u * self.vector.x, self.start.y + u * self.vector.y)
    
    def congruent_with(self, other):
        try:
            return isinstance(other, Line) and self.vector == other.vector and self.start in other
        except ZeroDivisionError:
            return False

class Ray(Line):
    def __repr__(self):
        return f'<Ray start:{self.start} vector:{self.vector}>'
    
    def intersects(self, line):
        determinant = self.determinant(line)
        if determinant:
            tr = (line.vector.x*(line.start.y - self.start.y) - line.vector.y*(line.start.x - self.start.x)) / determinant
            
            return determinant and tr >= 0
        else:
            return False

class Edge:
    def __init__(self, line, normal):
        self.line = line
        self.normal = normal
    
    def __repr__(self):
        return f'<Edge line:{self.line} normal:{self.normal}>'
    __str__=__repr__

class Area:
    def __init__(self, edges):
        self.edges = list(edges)
    
    def __repr__(self):
        return f'<Area edges:{self.edges}>'
    __str__=__repr__
    
    def __contains__(self, point):
        if len(self.edges) == 1:
            return Ray(point, self.edges[0].normal.reverse).intersects(self.edges[0].line)
        else:
            return all((point in x) for x in self.decomposition)
    
    def __and__(self, other):
        return self.intersection(other)
    
    def __ior__(self, other):
        return self.intersection_update(other)
    
    @classmethod
    def split_plane(cls, line, point):
        cw_side = cls([Edge(line, line.vector.clockwise)])
        ccw_side = cls([Edge(line, line.vector.counterclockwise)])
        
        if point in cw_side:
            return cw_side
        else:
            return ccw_side
    
    def intersection(self, other):
        return self.__class__(self.edges + other.edges)
    
    def intersection_update(self, other):
        self.edges.extend(other.edges)
    
    def subareas(self, size):
        yield from map(Area, self.rings(size))
    
    @property
    def all_subareas(self):
        for size in range(3, len(self.edges) + 1):
            yield from self.subareas(size)
    
    def rings(self, size=None):
        for sequence in permutations(self.edges, size or (len(self.edges) + 1)):
            sequence = list(sequence)
            
            if all(x.line.intersects(y.line) and not x.line.congruent_with(y.line) for x,y in zip(sequence, sequence[-1:] + sequence[:-1])):
                yield sequence
    
    @property
    def vertices(self):
        for ring in self.rings():
            for x,y in zip(ring, ring[:-1] + ring[:-1]):
                if x.line.intersects(y.line):
                    yield x.line & y.line
    
    @property
    def is_bounded(self): ###FIXME: returns true for everything
        #is there a set of edges that form a ring AND (only for convex areas) are all points in the set in the split planes defined by the edges?
        
        #this looks bizarre, but Area.__contains__ takes normals into account
        return any(all(vertex in subarea for vertex in subarea.vertices) for subarea in self.all_subareas)
    
    @property
    def decomposition(self):
        return (self.__class__([x]) for x in self.edges)

class Grid:
    def __init__(self, points):
        self.points = tuple(points)
        
        for point in self.points:
            point.grid = self
    
    def __repr__(self):
        return f'<Grid points:{self.points}>'
    __str__=__repr__
    
    def __getitem__(self, key):
        if isinstance(key, str):
            return next(x for x in self.points if x.name == key)
        elif isinstance(key, tuple):
            return next(x for x in self.points if (x.x, x.y) == key)
        elif isinstance(key, int):
            return self.points[key]
        else:
            return next(x for x in self.points if x == key)
