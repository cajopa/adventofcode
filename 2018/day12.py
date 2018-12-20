#!/usr/bin/env pypy3

from functools import reduce
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
    
    return Cavern(initial, rules)

def part1(data=None, test=False):
    '''
    After 20 generations, what is the sum of the numbers of all pots which contain a plant?
    '''
    
    # return reduce(lambda x,y: next(x), range(20), common_part(data, test)).score
    return common_part(data, test).run(20).score

def part2(data=None, test=None):
    '''
    After fifty billion (50000000000) generations, what is the sum of the numbers of all pots which contain a plant?
    '''
    
    return common_part(data, test).run(50*10**9).score


class Cavern:
    def __init__(self, pots, rules):
        self.pots = tuple(pots)
        self.rules = rules
        
        self.origin = 0
        self.history = {}
        
        print(self)
    
    def __repr__(self):
        return '<{} @{} {}>'.format(
            self.__class__.__name__,
            self.origin,
            ''.join(('X' if i==0 else '#') if x else ('o' if i==0 else '.') for i,x in zip(range(-self.origin, len(self.pots) - self.origin), self.pots))
        )
    
    def __str__(self):
        return self.__repr__()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.increment()
        
        print(self)
        
        return self
    
    def run(self, generations):
        head_of_cycle = self.brute_force(generations)
        
        if head_of_cycle:
            remaining_generations = self.skip_ahead(head_of_cycle, generations)
            
            for i in range(remaining_generations):
                self.increment()
                print(self)
        
        return self
    
    def brute_force(self, generations):
        for i in range(generations):
            self.increment()
            
            print(self)
            
            if self.pots in self.history:
                return self.pots
            else:
                self.history[self.pots] = (self.origin, len(self.history))
        
        return None
    
    def increment(self):
        self.pad_and_prune(4)
        
        self.pots = (False, False) + tuple(self.rules[tuple(self.pots[i-2:i+3])] for i in range(2, len(self.pots) - 3)) + (False, False)
        
        self.pad_and_prune(0)
    
    def skip_ahead(self, head_of_cycle, generations):
        #calculate length of cycle
        head_origin, head_position = self.history[head_of_cycle]
        cycle_length = len(self.history) - head_position
        
        #calculate change in origin from start to finish
        origin_delta = self.origin - head_origin
        
        #set origin to the future
        cycle_quantity, remaining_generations = divmod(generations - head_position, cycle_length)
        
        self.origin += (cycle_quantity - 1) * origin_delta
        
        print(f'skipped {cycle_quantity*cycle_length} generations')
        print(self)
        
        #return the quantity of remaining generations to brute force
        return remaining_generations
    
    def pad_and_prune(self, size):
        first_true = self.pots.index(True)
        last_true = list(reversed(self.pots)).index(True)
        
        self.pots = (False,)*size + self.pots[first_true:len(self.pots)-last_true] + (False,)*size
        self.origin += size - first_true
    
    @staticmethod
    def strip_list(list_):
        first_true = list_.index(True)
        last_true = list(reversed(list_)).index(True)
        
        return list_[first_true:len(list_)-last_true]
    
    @property
    def score(self):
        return sum(x * y for x,y in zip(range(-self.origin, len(self.pots) - self.origin), self.pots))


if __name__=='__main__':
    run_as_script(
        part1,
        {load('input/12.test'): 325},
        part2,
        {
            load('input/12.test.2.1'): None,
            load('input/12.test.2.2'): None,
        }
    )
