#!/usr/bin/env pypy3

from geometry import Vector
from util import run_as_script


DEBUG = False
INPUT = 320851
STARTING_SCORES = [3,7]


def part1(data=None):
    '''
    What are the scores of the ten recipes immediately after the number of recipes in your puzzle input?
    '''
    
    board = Scoreboard()
    
    if DEBUG:
        import time
        
        start_time = time.time()
        print(f'start time: {start_time}')
        
        to_return = ''.join(str(x) for x in board.run_until_10_more(data or INPUT))
        
        elapsed_time = time.time() - start_time
        
        print(f'elapsed time: {elapsed_time}s')
        
        return to_return
    else:
        return ''.join(str(x) for x in board.run_until_10_more(data or INPUT))

def part2(data=None):
    '''
    How many recipes appear on the scoreboard to the left of the score sequence in your puzzle input?
    '''
    
    return Scoreboard().run_until_sequence(data or str(INPUT))


class Scoreboard:
    def __init__(self):
        self.scores = list(STARTING_SCORES)
        self.positions = (0,1)
    
    def __str__(self):
        def inner():
            for i,v in enumerate(self.scores):
                if i == self.positions[0]:
                    yield f'({v})'
                elif i == self.positions[1]:
                    yield f'[{v}]'
                else:
                    yield f' {v} '
        
        return ''.join(inner())
    
    @property
    def elf1_score(self):
        return self.scores[self.positions[0]]
    
    @property
    def elf2_score(self):
        return self.scores[self.positions[1]]
    
    @property
    def new_scores(self):
        return self.elf1_score + self.elf2_score
    
    def increment(self):
        self.scores.extend(int(x) for x in str(self.new_scores))
        
        self.positions = tuple((x + self.scores[x] + 1) % len(self.scores) for x in self.positions)
    
    def run_until_length(self, length):
        if DEBUG:
            i = 0
            while len(self.scores) < length:
                i += 1
                if i % 1000 == 0:
                    print('.', end='', flush=True)
                self.increment()
        else:
            while len(self.scores) < length:
                self.increment()
    
    def run_until_10_more(self, length):
        self.run_until_length(length + 10)
        margin = len(self.scores) - length - 10
        
        return self.scores[-(10+margin):-margin or None]
    
    def run_until_sequence(self, sequence):
        sequence_length = len(sequence)
        
        while True:
            if self.scores[-sequence_length:] == sequence or self.scores[-sequence_length-1:-1] == sequence:
                break
            else:
                self.increment()
        
        return len(self.scores) - sequence_length


if __name__=='__main__':
    run_as_script(14, part1, part2)
