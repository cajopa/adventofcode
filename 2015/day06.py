import re


DEBUG = False


def load(input_filename):
    with open(input_filename, 'r') as f:
        for line in f:
            match = re.match(r'(?P<action>turn (?:on|off)|toggle) (?P<x0>\d+),(?P<y0>\d+) through (?P<x1>\d+),(?P<y1>\d+)', line.strip())
            
            groupdict = match.groupdict()
            
            if groupdict['action'] == 'turn on':
                action = lambda x: 1
            elif groupdict['action'] == 'turn off':
                action = lambda x: 0
            elif groupdict['action'] == 'toggle':
                action = lambda x: 1 - x
            else:
                raise ValueError('invalid action {}'.format(groupdict['action']))
            
            point0 = (int(groupdict['x0']), int(groupdict['y0']))
            point1 = (int(groupdict['x1']), int(groupdict['y1']))
            
            yield action, point0, point1

def run1(input_filename='input/day06'):
    return count_lights(follow_instructions(load(input_filename)))

def follow_instructions(instructions):
    grid = [[0] * 1000] * 1000
    
    for action, point0, point1 in instructions:
        for x in xrange(point0[0], point1[0]+1):
            for y in xrange(point0[1], point1[1]+1):
                grid[x][y] = action(grid[x][y])
    
    return grid

def count_lights(grid):
    return sum([sum(x) for x in grid])
