from collections import defaultdict


DEBUG = True


def load(input_filename):
    with open(input_filename, 'r') as f:
        return [x.strip() for x in f]

def run(input_filename, iterations):
    grid = Grid.from_text(load(input_filename))
    virus = Virus(grid)
    
    return sum(virus.burst() for i in range(iterations))

def run_short_example():
    return run('day22.input.example', 70) #should be 41

def run_example():
    return run('day22.input.example', 10000) #should be 5587

def run1():
    return run('day22.input', 10000)

def run2():
    pass


class Grid(defaultdict):
    def __init__(self):
        super().__init__(bool)
    
    def __str__(self):
        size = max(max(abs(x) for x,y in self.keys()), max(abs(y) for x,y in self.keys()))
        
        return '\n'.join(''.join(self[x,y] and '#' or '.' for x in range(-size, size+1)) for y in range(-size, size+1))
    
    @classmethod
    def from_text(cls, lines):
        to_return = cls()
        
        width = len(lines[0])
        height = len(lines)
        
        for y,line in enumerate(lines):
            for x,value in enumerate(line):
                to_return[x - width//2, y - height//2] = value == '#'
        
        return to_return
    
    @property
    def parity(self):
        return sum(self.values())

class Virus:
    '''
    If the current node is infected, it turns to its right. Otherwise, it turns to its left. (Turning is done in-place; the current node does not change.)
    If the current node is clean, it becomes infected. Otherwise, it becomes cleaned. (This is done after the node is considered for the purposes of changing direction.)
    The virus carrier moves forward one node in the direction it is facing.
    '''
    
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
    
    def infect(self):
        to_return = not self.grid[self.position]
        
        if DEBUG:
            print('try to infect: {}'.format(to_return and 'success' or 'failure'))
        
        self.grid[self.position] = to_return
        return to_return
    
    def move(self):
        self.position = tuple(map(sum, zip(self.position, self.direction)))
        
        if DEBUG:
            print('move to {}'.format(self.position))
    
    def burst(self):
        if self.grid[self.position]:
            self.turn_right()
        else:
            self.turn_left()
        
        to_return = self.infect()
        self.move()
        
        return to_return
