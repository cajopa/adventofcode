from itertools import chain, product

from kids.cache import cache


DEBUG = False

DEFAULT_INPUT = 'input/day18'
DEFAULT_STEPS = 100


def load(cls, input_filename=DEFAULT_INPUT):
    with open(input_filename, 'r') as f:
        return cls.from_text(f)

def run1():
    grid = load(Day1Grid)
    
    for i in range(DEFAULT_STEPS):
        if DEBUG:
            print('blit #{}'.format(i + 1))
        
        grid = grid.blit()
    
    return grid.number_on

def run2():
    pass


class Grid:
    registry = {}
    
    def __init__(self, flat_list):
        self.values = flat_list
    
    def __getitem__(self, key):
        x, y = key
        
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False
        else:
            return self.values[self.size * y + x]
    
    def __str__(self):
        return '\n'.join(''.join(self[x, y] and '#' or '.' for x in range(self.size)) for y in range(self.size))
    
    @classmethod
    def from_text(cls, lines):
        return cls.faux_new([x == '#' for x in chain.from_iterable(lines)])
    
    @classmethod
    def faux_new(cls, flat_list):
        key = tuple(flat_list)
        
        try:
            return cls.registry[key]
        except KeyError:
            to_return = cls(flat_list)
            cls.registry[key] = to_return
            return to_return
    
    @property
    def number_on(self):
        return len([None for x in self.values if x])
    
    @cache
    @property
    def size(self):
        return int(len(self.values) ** 0.5)
    
    def blit(self):
        def inner():
            for y in range(self.size):
                for x in range(self.size):
                    neighbors = self.count_neighbors(x, y)
                    yield self[x, y] and self.when_on_rule(neighbors) or self.when_off_rule(neighbors)
        
        return self.__class__(list(inner()))
    
    @cache
    def count_neighbors(self, x, y):
        return len([None for xoff,yoff in product([-1, 0, 1], repeat=2) if (xoff,yoff) != (0,0) and self[x+xoff, y+yoff]])
    
    def when_on_rule(self, neighbors):
        pass
    
    def when_off_rule(self, neighbors):
        pass


class Day1Grid(Grid):
    def when_on_rule(self, neighbors):
        return neighbors in (2, 3)
    
    def when_off_rule(self, neighbors):
        return neighbors == 3
