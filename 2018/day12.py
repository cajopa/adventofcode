#!/usr/bin/env pypy3

import re

from util import run_as_script
from datatypes import frozendict


def load(filename):
    with open(filename) as f:
        #initial state: #.#..#..###.###.#..###.#####...########.#...#####...##.#....#.####.#.#..#..#.#..###...#..#.#....##.
        first_line = f.readline().strip()
        initial_pattern = re.compile(r'initial state: (.+)')
        
        initial = tuple(x == '#' for x in initial_pattern.match(first_line).group(1))
        
        # #.### => .
        pattern = re.compile(r'(?P<predicate>.{5}) => (?P<consequent>.)')
        rules = frozendict()
        
        for line in f:
            line = line.strip()
            
            if line:
                match = pattern.match(line)
                
                if match:
                    rules[tuple(x == '#' for x in match.group('predicate'))] = match.group('consequent') == '#'
                else:
                    raise Exception('failed to parse line {!r}'.format(line))
        
        return initial, rules

def common_part(data, test):
    initial, rules = data or load('input/12.test' if test else 'input/12')
    
    return Board(initial, rules)

def part1(data=None, test=False):
    '''
    After 20 generations, what is the sum of the numbers of all pots which contain a plant?
    '''
    
    board = common_part(data, test)
    
    [None for _ in zip(board, range(20-1))]
    
    return board.score

def part2(data=None, test=None):
    '''
    After fifty billion (50000000000) generations, what is the sum of the numbers of all pots which contain a plant?
    '''
    
    board = common_part(data, test)
    
    [None for _ in zip(board, range(50*10**9-1))]
    
    return board.score


class Board:
    def __init__(self, states, rules):
        self.states = list(states)
        self.rules = rules
        
        self.origin = 0
        
        print(self)
    
    def __repr__(self):
        return '<{} {}>'.format(
            self.__class__.__name__,
            ''.join(('X' if i==0 else '#') if x else ('o' if i==0 else '.') for i,x in zip(range(-self.origin, len(self.states) - self.origin), self.states))
        )
    
    def __str__(self):
        return self.__repr__()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.pad_states(4)
        
        new_states = [self.rules[tuple(self.states[i-2:i+3])] for i in range(2, len(self.states) - 3)]
        
        ### NOTE: This assumes that a state is reachable where it doesn't change. This logic does not handle cycles!
        if self.strip_list(self.states) == self.strip_list(new_states):
            raise StopIteration
        else:
            self.states = new_states
        
        print(self)
        
        return self
    
    def pad_states(self, size):
        first_true = self.states.index(True)
        last_true = list(reversed(self.states)).index(True)
        
        self.states = [False]*size + self.states[first_true:len(self.states)-last_true] + [False]*size
        self.origin += size - first_true - 2
    
    @staticmethod
    def strip_list(list_):
        first_true = list_.index(True)
        last_true = list(reversed(list_)).index(True)
        
        return list_[first_true:len(list_)-last_true]
    
    @property
    def score(self):
        return sum(x * y for x,y in zip(range(-self.origin, len(self.states) - self.origin), self.states))


if __name__=='__main__':
    run_as_script(part1, {load('input/12.test'): 325}, part2, None)
