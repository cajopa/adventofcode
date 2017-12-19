from __future__ import print_function

import gmpy
from itertools import chain, product, count

from day10part2 import KnotHash


input_value = 'hwlqcszp'

# 11.2.3...
# .1.2.3.4.
# ....5.6..
# 7.8.55.9.
# .88.5....
# 88..5..88
# .8...8..8
# 88.8.88.8
# 888888888

example = [
    [1,1,0,2,0,3,0,0,0],
    [0,1,0,2,0,3,0,4,0],
    [0,0,0,0,5,0,6,0,0],
    [7,0,8,0,5,5,0,9,0],
    [0,8,8,0,5,0,0,0,0],
    [8,8,0,0,5,0,0,8,8],
    [0,8,0,0,0,8,0,0,8],
    [8,8,0,8,0,8,8,0,8],
    [8,8,8,8,8,8,8,8,8]
]

DEBUG = True


def run1(prefix=input_value):
    return sum(map(gmpy.popcount, chain(*(KnotHash('{}-{:d}'.format(prefix, row)).bindigest() for row in xrange(128)))))

def run2(prefix=input_value):
    value_grid = [boolify(intdigest(KnotHash('{}-{:d}'.format(prefix, x)))) for x in range(128)]
    
    if DEBUG:
        print('\n'.join([''.join(['#' if x else '.' for x in row]) for row in value_grid]))
    
    unmarked_cells = coordinate(value_grid)
    
    if DEBUG:
        print('number of unmarked cells: {}'.format(len(unmarked_cells)))
    
    region_count = 0
    while unmarked_cells:
        region_count += 1
        
        row, col = next(iter(unmarked_cells))
        
        visit(row, col, unmarked_cells)
        
        if DEBUG:
            print('number of unmarked cells: {}'.format(len(unmarked_cells)))
    
    return region_count

def intdigest(knot):
    return sum((x << (8*i) for i,x in enumerate(reversed(knot.bindigest()))))

def boolify(integer):
    return [bool(integer >> x & 0x1) for x in range(127,-1,-1)]

def coordinate(grid):
    to_return = set()
    
    for i,row in enumerate(grid):
        for j,cell in enumerate(row):
            if cell:
                to_return.add((i,j))
    
    return to_return

def visit(row, col, unmarked_cells):
    if (row, col) in unmarked_cells:
        unmarked_cells.remove((row, col))
        
        visit(row+1, col, unmarked_cells)
        visit(row-1, col, unmarked_cells)
        visit(row, col+1, unmarked_cells)
        visit(row, col-1, unmarked_cells)

def format_coords(coords, xsize, ysize):
    def format_rows():
        for row in xrange(ysize):
            yield ''.join(('#' if (row,col) in coords else ' ' for col in xrange(xsize)))
    
    return '\n'.join(format_rows())
