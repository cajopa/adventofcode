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

def part2(data=None):
    '''
    '''


class Scoreboard:
    def __init__(self):
        self.scores = STARTING_SCORES
        self.positions = [0,1]
    
    @property
    def elf1_score(self):
        return self._extract_score(self.positions[0])
    
    @property
    def elf2_score(self):
        return self._extract_score(self.positions[1])
    
    @property
    def new_scores(self):
        return self.elf1_score + self.elf2_score
    
    def increment(self):
        new_scores = self.new_scores
        
        if new_scores > 9:
            self.scores = self.scores * 100 + new_scores
        else:
            self.scores = self.scores * 10 + new_scores
    
    def _extract_score(self, position):
        return self.scores // 10**(self._calculate_digit_quantity(self.scores) - position - 1) % 10
    
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
