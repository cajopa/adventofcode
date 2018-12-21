#!/usr/bin/env pypy3

from itertools import cycle

from kids.cache import cache

from geometry import Vector
from util import run_as_script


DEBUG = False


def load(filename):
    with open(filename) as f:
        pass

def common_part(data, test):
    initial, rules = data or load('input/13.test' if test else 'input/13')
    
    return Cavern(initial, rules)

def part1(data=None, test=False):
    '''
    After following their respective paths for a while, the carts eventually crash. To help prevent
    crashes, you'd like to know the location of the first crash. Locations are given in X,Y
    coordinates, where the furthest left column is X=0 and the furthest top row is Y=0.
    '''
    

def part2(data=None, test=None):
    '''
    '''


class TrackSystem:
    def __init__(self, tracks):
        self.tracks = {x.coordinates: x for x in tracks}
        
        self.adopt()
    
    def __getitem__(self, key):
        return self.tracks.get(key)
    
    def __iter__(self):
        '''
        iterator for tracks in proper order
        '''
        
        pass
    
    def adopt(self):
        for track in self.tracks:
            track.system = self
    
    def tick(self):
        pass

class Track:
    def __init__(self, coordinates, connections):
        self.coordinates = coordinates
        self._connections = connections
        
        self.system = None
    
    @cache
    @property
    def connections(self):
        return [self.system[x] for x in self._connections]
    
    def next_direction(self, cart):
        raise NotImplementedError

class Straightaway(Track):
    def next_direction(self, cart):
        return cart.direction

class Corner(Track):
    def __init__(self, coordinates, connections):
        super().__init__(coordinates)
        
        self.directions = tuple(x - self.coordinates for x in self._connections)
    
    def next_direction(self, cart):
        return self.directions[1 - self.direction.index(cart.direction)]

class Intersection(Track):
    def next_direction(self, cart):
        return next(cart.intersection_direction)

class Cart:
    def __init__(self, initial_track, initial_direction):
        self.track = initial_track
        self.direction = initial_direction
        self.intersection_direction = cycle(self.direction.counterclockwise, self.direction.copy, self.direction.clockwise)
    
    def move(self):
        #move forward one
        #did I crash?
        #turn according to the track landed on
        pass

class Crashed(Exception):
    def __init__(self, cart):
        self.cart = cart
        
        super().__init__()


if __name__=='__main__':
    run_as_script(
        part1,
        {load('input/13.test'): (7,3)},
        part2,
        None
    )