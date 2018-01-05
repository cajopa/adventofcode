from itertools import chain
import re


DEBUG = False

ACTIONS1 = {
    'turn on': lambda x: True,
    'turn off': lambda x: False,
    'toggle': lambda x: (not x)
}

ACTIONS2 = {
    'turn on': lambda x: x+1,
    'turn off': lambda x: max(0, x-1),
    'toggle': lambda x: x+2
}


def load(input_filename):
    with open(input_filename, 'r') as f:
        for line in f:
            match = re.match(r'(?P<action>turn (?:on|off)|toggle) (?P<x0>\d+),(?P<y0>\d+) through (?P<x1>\d+),(?P<y1>\d+)', line.strip())
            
            groupdict = match.groupdict()
            
            point0 = (int(groupdict['x0']), int(groupdict['y0']))
            point1 = (int(groupdict['x1']), int(groupdict['y1']))
            
            yield groupdict['action'], point0, point1

def run1(input_filename='input/day06'):
    return count_lights(follow_instructions(load(input_filename), False, ACTIONS1))

def run2(input_filename='input/day06'):
    return total_brightness(follow_instructions(load(input_filename), 0, ACTIONS2))

def follow_instructions(instructions, initial_value, actions, size=1000):
    grid = [[initial_value for _ in xrange(size)] for _ in xrange(size)]
    
    # import pdb; pdb.set_trace()
    for action, point0, point1 in instructions:
        minx = min(point0[0], point1[0])
        maxx = max(point0[0], point1[0])
        miny = min(point0[1], point1[1])
        maxy = max(point0[1], point1[1])
        
        for x in xrange(minx, maxx+1):
            for y in xrange(miny, maxy+1):
                grid[x][y] = actions[action](grid[x][y])
                if DEBUG:
                    print x, y, grid[x][y]
    
    return grid

def count_lights(grid):
    return sum((len(filter(None, col)) for col in grid))

def total_brightness(grid):
    return sum(chain(*grid))
