#!/usr/bin/env pypy3

from itertools import product, chain
from time import time

from kids.cache import cache

from geometry import Point, Grid as GridBase
from util import run_as_script


POWER_LEVEL_TEST_DATA = {
    ((3,5),8): 4,
    ((122,79),57): -5,
    ((217,196),39): 0,
    ((101,153),71): 4,
}

TEST_DATA_1 = {
    18: ((33,45),29),
    42: ((21,61),30),
}

TEST_DATA_2 = {
    18: ((90,269),113,16),
    42: ((232,251),119,12),
}

INPUT = 5468


def load():
    return INPUT

def common_part(data=None):
    serial_number = data or load()
    
    return Grid(serial_number)

def part1(data=None):
    '''
    Your goal is to find the 3x3 square which has the largest total power. The square must be
    entirely within the 300x300 grid. Identify this square using the X,Y coordinate of its top-left
    fuel cell.
    
    What is the X,Y coordinate of the top-left fuel cell of the 3x3 square with the largest total power?
    '''
    
    grid = common_part(data=data)
    
    the_winner = max(grid.subgrids, key=lambda x: x.total_power)
    
    return the_winner.coordinates, the_winner.total_power

def part2(data=None):
    '''
    You discover a dial on the side of the device; it seems to let you select a square of any size,
    not just 3x3. Sizes from 1x1 to 300x300 are supported.
    
    What is the X,Y,size identifier of the square with the largest total power?
    '''
    
    grid = common_part(data=data)
    
    return max(grid.all_subgrid_scores, key=lambda x: x[2])


class GridBase:
    def __init__(self):
        self.size = 300
    
    def __getitem__(self, key):
        x,y = key
        
        return self.fuel_cells[x*self.size + y]
    
    @property
    def all_subgrids(self):
        'iterator for all NxN subgrids'
        
        return chain.from_iterable(self._subgrids(n) for n in range(1, self.size + 1))
    
    @property
    def all_subgrid_scores(self):
        for size in range(1, self.size + 1):
            yield from ((x.coordinates, size, x.total_power) for x in self._subgrids(size))
    
    def _subgrids(self, size):
        print(f'evaluating subgrids of size {size}x{size}...', end='')
        
        start_time = time()
        
        for topleft_x in range(300-size+1):
            for topleft_y in range(300-size+1):
                yield Subgrid((topleft_x+1, topleft_y+1), size, (self[x, y] for x,y in product(range(topleft_x, topleft_x+size), range(topleft_y, topleft_y+size))))
        
        end_time = time()
        
        print(f'took {end_time - start_time}s')
        
        Subgrid.prune_cache(size - 1)


class Grid(GridBase):
    def __init__(self, serial_number):
        super().__init__()
        
        self.fuel_cells = [self.calculate_power_level(x, y, serial_number) for x,y in product(range(300), repeat=2)]
    
    @classmethod
    def calculate_power_level(cls, x, y, serial_number):
        x += 1
        y += 1
        
        rack_id = x + 10
        
        #Begin with a power level of the rack ID times the Y coordinate.
        to_return = rack_id * y
        
        #Increase the power level by the value of the grid serial number (your puzzle input).
        to_return += serial_number
        
        #Set the power level to itself multiplied by the rack ID.
        to_return *= rack_id
        
        #Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
        to_return = to_return // 100 % 10
        
        #Subtract 5 from the power level.
        to_return -= 5
        
        return to_return
    
    @property
    def subgrids(self):
        'iterator for 3x3 subgrids'
        
        return self._subgrids(3)

class Subgrid(GridBase):
    power_cache = {}
    
    def __init__(self, coordinates, size, fuel_cells):
        self.coordinates = coordinates
        self.size = size
        self.fuel_cells = list(fuel_cells)
    
    @property
    def total_power(self):
        if self.size == 1:
            to_return = self.fuel_cells[0]
        else:
            #uses the one-smaller subgrid rooted at the same location and fills with singles
            # time complexity O(2*n)
            
            to_return = (
                self.subgrid(self.coordinates[0], self.coordinates[1], self.size-1) +
                sum(self[x,self.size-1] for x in range(self.size-1)) +
                sum(self[self.size-1,y] for y in range(self.size-1)) +
                self[self.size-1, self.size-1]
            )
        
        self.power_cache[self.coordinates, self.size] = to_return
        
        return to_return
    
    @classmethod
    def prune_cache(cls, maxsize):
        to_delete = [(c,s) for c,s in cls.power_cache.keys() if s < maxsize]
        
        for k in to_delete:
            del cls.power_cache[k]
    
    def subgrid(self, left, top, size):
        key = ((left,top), size)
        
        if key in self.power_cache:
            return self.power_cache[key]
        else:
            add_coords = lambda x,y: tuple(map(sum, zip(self.coordinates, (x,y))))
            
            return self.__class__(add_coords(left, top), size, [self[x,y] for x,y in product(range(left, left + size), range(top + size))])


if __name__=='__main__':
    run_as_script(part1, TEST_DATA_1, part2, TEST_DATA_2)
