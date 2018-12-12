#!/usr/bin/env python

from itertools import cycle
import re


TEST_DATA = {
    (9,25): 32,
    (10,1618): 8317,
    (13,7999): 146373,
    (17,1104): 2764,
    (21,6111): 54718,
    (30,5807): 37305,
}


def load(input_filename):
    with open(input_filename, 'r') as f:
        #432 players; last marble is worth 71019 points
        match = re.match(r'(?P<players>\d+) players; last marble is worth (?P<maxpoints>\d+) points', f.read().strip())
        
        return int(match.group('players')), int(match.group('maxpoints'))

def common_part(data=None):
    players, maxpoints = data or load('input/9')
    
    return Field(players, maxpoints)

def part1(data=None):
    '''
    What is the winning Elf's score?
    '''
    
    field = common_part(data=data)
    
    #plays the game
    list(field)
    
    return max(field.player_scores)

def test1():
    passed = []
    failed = {}
    
    for k,v in TEST_DATA.items():
        actual_value = part1(k)
        
        if actual_value == v:
            passed.append(k)
        else:
            failed[k] = (v, actual_value)
    
    return passed, failed

def part2(data=None):
    '''
    '''


class Field:
    def __init__(self, player_quantity, marble_quantity):
        self.player_quantity = player_quantity
        self.marble_quantity = marble_quantity
        
        self.player_scores = None
        self.ring = None
        self.current_iter = None
        self.current_position = None
    
    def __iter__(self):
        #pre-assign players to marbles
        self.current_iter = zip(cycle(range(self.player_quantity)), range(1, self.marble_quantity+1))
        self.current_position = 0
        self.ring = Ring([0])
        self.player_scores = [0]*self.player_quantity
        
        return self
    
    def __next__(self):
        for i in range(1,24):
            ### NOTE: can throw StopIteration - it's fine for that to bubble up
            player, marble = next(self.current_iter)
            
            if len(self.ring) == 1:
                ### TODO: why does this need special casing? There is an edge case somewhere.
                self.ring.append(marble)
                self.current_position = 1
            #However, if the marble that is about to be placed has a number which is a multiple of 23, something entirely different happens.
            elif i % 23 == 0:
                #First, the current player keeps the marble they would have placed, adding it to their score.
                self.player_scores[player] += marble
                
                #In addition, the marble 7 marbles counter-clockwise from the current marble is removed from the circle and also added to the current player's score.
                self.player_scores[player] += self.ring.pop(self.current_position - 7)
                
                #The marble located immediately clockwise of the marble that was removed becomes the new current marble.
                self.current_position -= 7
            else:
                #Each Elf takes a turn placing the lowest-numbered remaining marble into the circle between the marbles that are 1 and 2 marbles clockwise of the current marble.
                #The marble that was just placed then becomes the current marble.
                self.current_position = self.ring.insert(self.current_position + 2, marble)
        
        return self

class Ring(list):
    def __getitem__(self, index):
        if isinstance(index, slice):
            ### IMPORTANT: known issue where the slice would wrap around the end
            start = index.start and (index.start % len(self))
            stop = index.stop and (index.stop % len(self))
            
            index = slice(start, stop, index.step)
        else:
            index %= len(self)
        
        return super().__getitem__(index)
    
    def insert(self, index, value):
        index %= len(self)
        
        super().insert(index, value)
        
        return index
    
    def pop(self, index):
        return super().pop(index % len(self))


if __name__=='__main__':
    from pprint import pformat
    import argparse
    import sys
    
    parser = argparse.ArgumentParser()
    parser.add_argument('part', type=int, help='which part to run')
    parser.add_argument('--test', action='store_true', help='run in test mode')
    
    args = parser.parse_args()
    
    if args.part == 1:
        if args.test:
            passed, failed = test1()
            
            print(f'passed: {pformat(passed)}')
            print(f'failed:\n{pformat(failed, indent=2)}')
        else:
            print(part1())
    elif args.part == 2:
        if args.test:
            passed, failed = test2()
            
            print(f'passed: {pformat(passed)}')
            print(f'failed:\n{pformat(failed, indent=2)}')
        else:
            print(part2())
    else:
        print(f'invalid part {args.part}', file=sys.stderr)
        sys.exit(1)
