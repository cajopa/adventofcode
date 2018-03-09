from collections import defaultdict
from enum import Enum

from kids.cache import cache


DEBUG = True


def load(input_filename):
    with open(input_filename, 'r') as f:
        return [x.strip() for x in f]

def run(input_filename, iterations, grid_cls):
    grid = grid_cls.from_text(load(input_filename))
    
    return sum(grid.virus.burst() for i in range(iterations))

def run1_short_example():
    return run('day22.input.example', 70, Grid1) #should be 41

def run1_example():
    return run('day22.input.example', 10000, Grid1) #should be 5587

def run1():
    return run('day22.input', 10000, Grid1) #result with the input given: 5223

def run2_short_example():
    return run('day22.input.example', 100, Grid2) #should be 26

def run2_example():
    return run('day22.input.example', 10000000, Grid2) #should be 2511944

def run2():
    return run('day22.input', 10000000, Grid2) #result with the input given: 2511456


class State(Enum):
    @cache
    @property
    def symbol_map(self):
        return {k: v for k,v in zip(self.symbols, self.__members__.values())}
    
    @cache
    @property
    def reverse_symbol_map(self):
        return {v: k for k,v in zip(self.symbols, (x.value for x in self.__members__.values()))}
    
    @classmethod
    def from_symbol(cls, symbol):
        if symbol == '.':
            return cls.CLEAN
        elif symbol == '#':
            return cls.INFECTED
        elif symbol == 'W':
            return cls.WEAKENED
        elif symbol == 'F':
            return cls.FLAGGED
    
    @property
    def symbol(self):
        return self.reverse_symbol_map()[self.value]
    
    def next(self):
        pass
    
    @property
    def default(self):
        pass
    
    @property
    def symbols(self):
        pass


class Day1State(State):
    CLEAN = 0
    INFECTED = 1
    
    DEFAULT = CLEAN
    
    @property
    def symbols(self):
        return ('.', '#')
    
    def next(self):
        if self == self.__class__.CLEAN:
            return self.__class__.INFECTED
        else:
            return self.__class__.CLEAN

class Day2State(State):
    CLEAN = 0
    INFECTED = 1
    WEAKENED = 2
    FLAGGED = 3
    
    DEFAULT = CLEAN
    
    @property
    def symbols(self):
        return ('.', '#', 'W', 'F')
    
    def next(self):
        if self == self.__class__.CLEAN:
            return self.__class__.WEAKENED
        elif self == self.__class__.WEAKENED:
            return self.__class__.INFECTED
        elif self == self.__class__.INFECTED:
            return self.__class__.FLAGGED
        elif self == self.__class__.FLAGGED:
            return self.__class__.CLEAN


class BaseGrid(defaultdict):
    enum_cls = None
    virus_cls = None
    
    def __init__(self):
        super().__init__(lambda: self.enum_cls.DEFAULT)
        
        self.virus = self.virus_cls(self)
    
    def __str__(self):
        size = max(max(abs(x) for x,y in self.keys()), max(abs(y) for x,y in self.keys()))
        
        return '\n'.join(''.join(self[x,y].symbol for x in range(-size, size+1)) for y in range(-size, size+1))
    
    @classmethod
    def from_text(cls, lines):
        to_return = cls()
        
        width = len(lines[0])
        height = len(lines)
        
        for y,line in enumerate(lines):
            for x,value in enumerate(line):
                to_return[x - width//2, y - height//2] = cls.enum_cls.from_symbol(value)
        
        return to_return
    
    @property
    def parity(self):
        return sum(self.values())

class BaseVirus:
    DIRECTIONS = {
        (0,-1): 'up',
        (1,0): 'right',
        (0,1): 'down',
        (-1,0): 'left'
    }
    
    def __init__(self, grid):
        self.position = (0,0)
        self.direction = (0,-1)
        self.grid = grid
    
    def turn_right(self):
        if DEBUG:
            print('turn right: ', end='')
        
        x,y = self.direction
        self.direction = ((x+y)*(abs(x)-1), (x+y)*(1-abs(y)))
        
        if DEBUG:
            print('now facing {}'.format(self.DIRECTIONS[self.direction]))
    
    def turn_left(self):
        if DEBUG:
            print('turn left: ', end='')
        
        x,y = self.direction
        self.direction = ((x+y)*(1-abs(x)), (x+y)*(abs(y)-1))
        
        if DEBUG:
            print('now facing {}'.format(self.DIRECTIONS[self.direction]))
    
    def move(self):
        self.position = tuple(map(sum, zip(self.position, self.direction)))
        
        if DEBUG:
            print('move to {}'.format(self.position))
    
    def turn(self):
        pass
    
    def infect(self):
        next_value = self.grid[self.position].next()
        
        if DEBUG:
            print('try to infect: {}'.format('success' if next_value == self.grid.enum_cls.INFECTED else 'failure'))
        
        self.grid[self.position] = next_value
        
        return next_value == self.grid.enum_cls.INFECTED
    
    def burst(self):
        self.turn()
        
        to_return = self.infect()
        self.move()
        
        return to_return

class Virus1(BaseVirus):
    '''
    If the current node is infected, it turns to its right. Otherwise, it turns to its left. (Turning is done in-place; the current node does not change.)
    If the current node is clean, it becomes infected. Otherwise, it becomes cleaned. (This is done after the node is considered for the purposes of changing direction.)
    The virus carrier moves forward one node in the direction it is facing.
    '''
    
    def turn(self):
        if self.grid[self.position] == self.grid.enum_cls.INFECTED:
            self.turn_right()
        else:
            self.turn_left()

class Virus2(BaseVirus):
    '''
    Decide which way to turn based on the current node:
        If it is clean, it turns left.
        If it is weakened, it does not turn, and will continue moving in the same direction.
        If it is infected, it turns right.
        If it is flagged, it reverses direction, and will go back the way it came.
    Modify the state of the current node, as described above.
    The virus carrier moves forward one node in the direction it is facing.
    '''
    
    def turn_around(self):
        if DEBUG:
            print('turn around: ', end='')
        
        x,y = self.direction
        self.direction = -x, -y
        
        if DEBUG:
            print('now facing {}'.format(self.DIRECTIONS[self.direction]))
    
    def turn_straight(self):
        if DEBUG:
            print('not turning: still facing {}'.format(self.DIRECTIONS[self.direction]))
    
    def turn(self):
        current_value = self.grid[self.position]
        
        if current_value == self.grid.enum_cls.CLEAN:
            self.turn_left()
        elif current_value == self.grid.enum_cls.WEAKENED:
            self.turn_straight()
        elif current_value == self.grid.enum_cls.INFECTED:
            self.turn_right()
        elif current_value == self.grid.enum_cls.FLAGGED:
            self.turn_around()
        else:
            raise Exception('how the shit did you get here? current_value: {}'.format(current_value))

class Grid1(BaseGrid):
    enum_cls = Day1State
    virus_cls = Virus1

class Grid2(BaseGrid):
    enum_cls = Day2State
    virus_cls = Virus2
