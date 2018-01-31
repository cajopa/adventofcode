from collections import defaultdict
from itertools import product, chain
from string import ascii_uppercase as LETTERS


DEBUG = True


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
                self.move(new_position)
                
                if new_value in LETTERS:
                    yield new_value
            else:
                new_new_position, new_new_value = self.peek(position=new_position)
                
                if new_new_value in chain(self.VALID_MOVES[self.direction], LETTERS):
                    self.move(new_new_position)
                    
                    if new_new_value in LETTERS:
                        yield new_new_value
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
        
        if self.grid.get(self.position) == self.CROSSROAD:
            self.direction = self.whichway()
        
        if DEBUG:
            print('{} {} {}'.format(new_position, self.DIRECTION_NAMES[self.direction], self.grid.get(new_position)))
    
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
