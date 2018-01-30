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



class RGrid:
    def __init__(self, flat_list):
        self.cells = defaultdict(lambda: None)
        
        size = int(len(flat_list) ** 0.5)
        value_iter = iter(flat_list)
        
        #first pass for filling in values
        for y in range(size):
            for x in range(size):
                self.cells[x, y] = Automaton(next(value_iter), None)
        
        #second pass for hooking up neighbors
        for y in range(size):
            for x in range(size):
                self.cells[x,y].neighbors = [self.cells[x+xoff, y+yoff] for xoff, yoff in product([-1, 0, 1], repeat=2) if (xoff,yoff) != (0,0) and self.cells[x, y]]
    
    def __str__(self):
        return '\n'.join(''.join(self.cells[x, y] and '#' or '.' for x in range(self.size)) for y in range(self.size))
    
    @classmethod
    def from_text(cls, lines):
        return cls([x == '#' for x in chain.from_iterable(lines)])
    
    def blit(self):
        self.cells[0, 0].blit()


class Automaton:
    def __init__(self, value, neighbors):
        self.visited = False
        
        self.value = value
        self.neighbors = neighbors
    
    def visit(self):
        'visit neighbors recursively'
        
        if not self.visited:
            for neighbor in self.neighbors:
                neighbor.visit()
            
            self.visited = True
    
    def unvisit(self):
        'unvisit neighbors recursively'
        
        if self.visited:
            for neighbor in self.neighbors:
                neighbor.unvisit()
            
            self.visited = False
    
    def blit(self):
        'return new self with determined state and connected to new neighbors'
        
        #FIXME: infinite recursion
        return self.__class__(self.newval, [x.blit() for x in self.neighbors])
    
    @property
    def newval(self):
        'determine the new value my successor will take'
        
        number_of_live_neighbors = len([None for x in self.neighbors if x.value])
        
        return self.value and number_of_live_neighbors in (2,3) or number_of_live_neighbors == 3
