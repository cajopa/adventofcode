import math


puzzle_input = 265149

#sum of squares: f(n) = n/6 * (n + 1) * (2*n + 1) = n**3/3 + n**2/2 + n/6
#the down-right diagonal consists of all squares of natural, odd numbers

#proposal:
# given x
# find s
## s >= x
## s = xs ** 2 //xs is a natural, odd number
# ???



def manhattan_distance(point0, point1):
    return abs(point0[0] - point1[0]) + abs(point0[1] - point1[1])

def corners(root):
    square = root**2
    return square, square-(root-1), square-2*(root-1), square-3*(root-1)

def find_least_containing_square_root(value):
    return int(math.ceil((value**0.5 - 1) / 2) * 2 + 1)

def find_cell(value):
    root = find_least_containing_square_root(value)
    downright, downleft, upleft, upright = corners(root)
    halfroot = root / 2
    
    if value > downleft:
        return value - downright + halfroot, -halfroot
    elif value > upleft:
        return -halfroot, downleft - value - halfroot
    elif value > upright:
        return upleft - value - halfroot, halfroot
    else:
        return halfroot, value - upright + halfroot

def origin_distance(value):
    return manhattan_distance((0,0), find_cell(value))
