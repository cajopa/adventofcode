#!/usr/bin/env pypy3

from itertools import cycle, chain

from geometry import Vector
from util import run_as_script


DEBUG = False
INPUT = 320851
STARTING_SCORES = 37


def part1(data=None):
    '''
    What are the scores of the ten recipes immediately after the number of recipes in your puzzle input?
    '''
    
    board = Scoreboard()
    
    board.run_until_length(data)
    
    return '{:010d}'.format(board.plus_10)

def part2(data=None):
    '''
    '''


class Scoreboard:
    def __init__(self):
        self.scores = STARTING_SCORES
        self.positions = [0,1]
    
    def __len__(self):
        return self._calculate_digit_quantity(self.scores)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, _ = index.indices(len(self))
        else:
            start, stop = index, index+1
        
        length = stop - start
        
        right_shifted = self.scores // 10**(len(self) - start - length)
        
        return right_shifted % 10**(length)
    
    @property
    def elf1_score(self):
        return self[self.positions[0]]
    
    @property
    def elf2_score(self):
        return self[self.positions[1]]
    
    @property
    def new_scores(self):
        return self.elf1_score + self.elf2_score
    
    @property
    def plus_10(self):
        old_length = len(self)
        self.run_until_length(old_length + 10)
        new_length = len(self)
        
        position = -(new_length - old_length - 10)
        
        return self[position:position+10]
    
    def increment(self):
        new_scores = self.new_scores
        
        if new_scores > 9:
            self.scores = self.scores * 100 + new_scores
        else:
            self.scores = self.scores * 10 + new_scores
    
    def run_until_length(self, length):
        while len(self) < length:
            self.increment()
    
    @classmethod
    def _calculate_digit_quantity(cls, value):
        if value >= 1000:
            return 3 + cls._calculate_digit_quantity(value // 1000)
        elif value >= 100:
            return 2 + cls._calculate_digit_quantity(value // 100)
        elif value >= 10:
            return 1 + cls._calculate_digit_quantity(value // 10)
        elif value >= 0:
            return 1
        else:
            return -1


if __name__=='__main__':
    run_as_script(14)
