#!/usr/bin/env python

from itertools import product, chain

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
    
    the_winner = max(grid.all_subgrids, key=lambda x: x.total_power)
    
    return the_winner.coordinates, the_winner.total_power, the_winner.size


class Grid:
    def __init__(self, serial_number):
        self.fuel_cells = [self.calculate_power_level(x, y, serial_number) for x,y in product(range(300), repeat=2)]
    
    def __getitem__(self, key):
        x,y = key
        
        return self.fuel_cells[x*300 + y]
    
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
    
    @property
    def all_subgrids(self):
        'iterator for all NxN subgrids'
        
        return chain.from_iterable(self._subgrids(n) for n in range(1,301))
    
    def _subgrids(self, size):
        print(f'evaluating subgrids of size {size}x{size}')
        
        for topleft_x in range(300-size+1):
            for topleft_y in range(300-size+1):
                yield Subgrid((topleft_x+1, topleft_y+1), (self[x, y] for x,y in product(range(topleft_x, topleft_x+size), range(topleft_y, topleft_y+size))))

class Subgrid:
    def __init__(self, coordinates, fuel_cells):
        self.coordinates = coordinates
        self.fuel_cells = list(fuel_cells)
    
    @property
    def total_power(self):
        return sum(self.fuel_cells)


# class Grid(GridBase):
#     def __init__(self, serial_number):
#         super().__init__(FuelCell(x,y,serial_number) for x,y in product(range(300), repeat=2))
    
#     @property
#     def subgrids(self):
#         'iterator for 3x3 subgrids'
        
#         ### NOTE: it's ok (and good) that the points passed to Subgrid aren't copies
        
#         for topleft_x in range(300-2):
#             for topleft_y in range(300-2):
#                 yield Subgrid((self.points_by_coords[x] for x in product(range(topleft_x, topleft_x+3), range(topleft_y, topleft_y+3))))
    
#     def parentify_points(self):
#         pass ### intentional

# class Subgrid(GridBase):
#     @cache(key=id)
#     @property
#     def total_power(self):
#         return sum(x.power_level for x in self.points)
    
#     @property
#     def coordinates(self):
#         'Identify this square using the X,Y coordinate of its top-left fuel cell.'
        
#         return Point(min(x.x for x in self.points), min(x.y for x in self.points))
    
#     def parentify_points(self):
#         pass ### intentional

# class FuelCell(Point):
#     def __init__(self, x, y, serial_number):
#         super().__init__(x, y)
        
#         self.rack_id = x * 10
#         self.power_level = self.calculate_power_level(serial_number)
    
#     def calculate_power_level(self, serial_number):
#         #Begin with a power level of the rack ID times the Y coordinate.
#         to_return = self.rack_id * self.y
        
#         #Increase the power level by the value of the grid serial number (your puzzle input).
#         to_return += serial_number
        
#         #Set the power level to itself multiplied by the rack ID.
#         to_return *= self.rack_id
        
#         #Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
#         to_return = to_return // 100 % 10
        
#         #Subtract 5 from the power level.
#         to_return -= 5
        
#         return to_return


if __name__=='__main__':
    run_as_script(part1, TEST_DATA_1, part2, TEST_DATA_2)
