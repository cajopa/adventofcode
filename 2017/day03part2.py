def get_neighbors(x, y, grid):
    return (
        grid.get((x+1, y), 0),
        grid.get((x+1, y+1), 0),
        grid.get((x, y+1), 0),
        grid.get((x-1, y+1), 0),
        grid.get((x-1, y), 0),
        grid.get((x-1, y-1), 0),
        grid.get((x, y-1), 0),
        grid.get((x+1, y-1), 0))

def display_grid(grid, ring):
    from math import log10, ceil
    
    max_length = max([int(ceil(log10(x+1))) for x in grid.itervalues()])
    
    for y in range(ring, -ring-1, -1):
        print ' '.join(['{: >{align}d}'.format(i, align=max_length) for i in [grid.get((x, y), 0) for x in range(-ring, ring+1)]])
    
    print

def populate_grid(goal):
    x,y = 1,0
    current = 1
    ring = 1
    grid = {(0,0): 1}
    
    while current <= goal:
        current = sum(get_neighbors(x, y, grid))
        grid[(x,y)] = current
        display_grid(grid, ring)
        
        old_x, old_y = x, y
        
        if x == ring:
            if y == -ring: #end of ring
                x += 1
                ring += 1
            elif y == ring: #corner - leftward-bound
                x -= 1
            else: #upward-bound
                y += 1
        elif y == ring:
            #already handled top-right corner
            if x == -ring: #corner - downward-bound
                y -= 1
            else: #leftward-bound
                x -= 1
        elif x == -ring:
            #already handled top-left corner
            if y == -ring: #corner - rightward-bound
                x += 1
            else: #downward-bound
                y -= 1
        elif y == -ring:
            #already handled both corners
            #rightward-bound
            x += 1
    
    return old_x, old_y, current
