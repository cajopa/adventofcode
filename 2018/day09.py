#!/usr/bin/env python

from itertools import cycle, chain
import re

from util import run_as_script


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

def part2(data=None):
    '''
    What would the new winning Elf's score be if the number of the last marble were 100 times larger?
    
    Different interpretations of this question exist:
      - only the last marble changes, value is 100*x             NO - MANUALLY TESTED
      - only the last marble changes, value is 101*x (large*r*)  NO - MANUALLY TESTED
      - the size of the marble pool is 100*l <================== THIS ONE
      - the size of the marble pool is 101*l (large*r*)
    '''
    
    field = common_part(data=data)
    
    field.marble_quantity *= 100
    
    list(field)
    
    return max(field.player_scores) #returns 3338341690 (takes forever to run currently)


class Field:
    def __init__(self, player_quantity, marble_quantity):
        self.player_quantity = player_quantity
        self.marble_quantity = marble_quantity
        
        self.player_scores = None
        self.ring = None
        self.current_iter = None
        self.position = None
        self.round = None
    
    def __iter__(self):
        #pre-assign players to marbles
        self.current_iter = zip(cycle(range(self.player_quantity)), range(1, self.marble_quantity+1))
        self.position = 0
        self.round = 0
        self.ring = Ring([0])
        self.player_scores = [0]*self.player_quantity
        
        return self
    
    def __next__(self):
        self.round += 1
        
        ### NOTE: can throw StopIteration - it's fine for that to bubble up
        player, marble = next(self.current_iter)
        
        #However, if the marble that is about to be placed has a number which is a multiple of 23, something entirely different happens.
        if self.round % 23 == 0:
            #First, the current player keeps the marble they would have placed, adding it to their score.
            self.player_scores[player] += marble
            # print(f'player {player} keeps marble #{marble} @{self.position}')
            
            #In addition, the marble 7 marbles counter-clockwise from the current marble is removed from the circle and also added to the current player's score.
            self.player_scores[player] += self.ring.pop(self.position - 7)
            # popped_marble = self.ring.pop(self.position - 7)
            # self.player_scores[player] += popped_marble
            # print(f'player {player} also gets marble #{popped_marble} @{self.position - 7}')
            
            #The marble located immediately clockwise of the marble that was removed becomes the new current marble.
            ### NOTE: position needs to be relative to the *previous* length of the ring
            self.position = (self.position - 7) % (len(self.ring) + 1)
        else:
            #Each Elf takes a turn placing the lowest-numbered remaining marble into the circle between the marbles that are 1 and 2 marbles clockwise of the current marble.
            self.ring.insert(self.position + 2, marble)
            
            #The marble that was just placed then becomes the current marble.
            ### NOTE: position needs to be relative to the *previous* length of the ring
            self.position = (self.position + 2) % (len(self.ring) - 1)
        
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
    
    def __add__(self, other):
        return self.__class__(chain(self, other))
    
    def insert(self, index, value):
        super().insert(index % len(self), value)
    
    def pop(self, index):
        return super().pop(index % len(self))
    
    def rotate(self, distance):
        '''
        Negative distance is leftward, positive is rightward.
        '''
        
        if distance == 0:
            return self.__class__(self)
        else:
            return self[-distance:] + self[:-distance]
    
    def align(self, target):
        return self.rotate(-self.index(target))


if __name__=='__main__':
    run_as_script(part1, TEST_DATA, part2, {})
