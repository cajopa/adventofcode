DEBUG = True

DIRECTIONS = {
    'n': (-1, 1, 0),
    'ne': (0, 1, -1),
    'se': (1, 0, -1),
    's': (1, -1, 0),
    'sw': (0, -1, 1),
    'nw': (-1, 0, 1)
}


def load(input_filename='day11.input'):
    with open(input_filename, 'r') as f:
        return f.read().strip().split(',')

def run1():
    return find_shortest(walk(load()))

def run2():
    return find_farthest(load())


def walk(directions):
    return reduce(move, directions, (0,0,0))

def move(position, direction):
    return map(sum, zip(position, DIRECTIONS[direction]))

def find_shortest(position):
    return max(map(abs, position))

def find_farthest(directions):
    position = (0, 0, 0)
    max_distance = 0
    
    for direction in directions:
        position = move(position, direction)
        distance = find_shortest(position)
        
        if distance > max_distance:
            max_distance = distance
    
    return max_distance
