from collections import defaultdict
from itertools import product, chain
from string import ascii_uppercase as LETTERS


DEBUG = True
DEFAULT_INPUT = 'day19.input'
EXAMPLE_INPUT = 'day19.input.example'


def load(cls, input_filename=DEFAULT_INPUT):
    with open(input_filename, 'r') as f:
        return cls(f.read())

def run1(input_filename=DEFAULT_INPUT):
    return ''.join(load(Day1Route, input_filename))

def run2(input_filename=DEFAULT_INPUT):
    return sum(load(Day2Route, input_filename))


class Route:
    VERTICAL = '|'
    HORIZONTAL = '-'
    CROSSROAD = '+'
    EMPTY = ' '
    OUTOFBOUNDS = None
    
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    DIRECTION_NAMES = {
        UP: 'UP',
        DOWN: 'DOWN',
        LEFT: 'LEFT',
        RIGHT: 'RIGHT',
    }
    
    VALID_MOVES = {
        UP: (VERTICAL, CROSSROAD),
        DOWN: (VERTICAL, CROSSROAD),
        LEFT: (HORIZONTAL, CROSSROAD),
        RIGHT: (HORIZONTAL, CROSSROAD),
    }
    
    
    def __init__(self, text):
        self.grid = defaultdict(lambda: None, (((x,y),vv) for y,v in enumerate(text.split('\n')) for x,vv in enumerate(v)))
        self.position = self.beginning
        self.direction = self.DOWN
    
    def __iter__(self):
        'traverse the route, collecting letters along the way'
        
        if DEBUG:
            print('{} {} |'.format(self.position, self.DIRECTION_NAMES[self.direction]))
        
        while True:
            new_position, new_value = self.peek()
            
            if new_value in chain(self.VALID_MOVES[self.direction], LETTERS):
                yield from self.move(new_position)
            else:
                new_new_position, new_new_value = self.peek(position=new_position)
                
                if new_new_value in chain(self.VALID_MOVES[self.direction], LETTERS):
                    yield from self.move(new_position)
                    
                    #NOTE: the following would be potentially much more efficient,
                    #      and always as correct, but would throw off the number of steps
                    #yield from self.move(new_new_position)
                else:
                    break
    
    def peek(self, direction=None, position=None):
        'gets the value of the grid in the indicated direction, or None if out of bounds'
        
        direction = direction or self.direction
        position = position or self.position
        
        new_position = tuple(map(sum, zip(position, direction)))
        
        return new_position, self.grid.get(new_position)
    
    def move(self, new_position):
        self.position = new_position
        
        new_value = self.grid.get(self.position)
        
        if new_value == self.CROSSROAD:
            self.direction = self.whichway()
        
        if DEBUG:
            print('{} {} {}'.format(new_position, self.DIRECTION_NAMES[self.direction], self.grid.get(new_position)))
        
        yield from self.post_move()
    
    def post_move(self):
        pass
    
    def whichway(self, position=None):
        position = position or self.position
        
        if self.direction in (self.UP, self.DOWN):
            possible_directions = (self.LEFT, self.RIGHT)
        else:
            possible_directions = (self.UP, self.DOWN)
        
        for direction in possible_directions:
            new_position, new_value = self.peek(direction)
            
            if new_value not in (self.EMPTY, self.OUTOFBOUNDS):
                return direction
    
    @property
    def beginning(self):
        return next(k for k,v in self.grid.items() if k[1] == 0 and v == self.VERTICAL)


class Day1Route(Route):
    def post_move(self):
        new_value = self.grid.get(self.position)
        
        if new_value in LETTERS:
            yield new_value
        else:
            yield ''


class Day2Route(Route):
    def __iter__(self):
        yield 1
        
        yield from super(Day2Route, self).__iter__()
    
    def post_move(self):
        new_value = self.grid.get(self.position)
        
        yield 1
