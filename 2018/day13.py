#!/usr/bin/env pypy3

from itertools import cycle, chain

from geometry import Vector
from util import run_as_script


DEBUG = False


class load:
    def __init__(self, filename):
        self.tracks = []
        self.carts = []
        
        with open(filename) as f:
            prior = None
            
            for y, line in enumerate(f):
                for x, char in enumerate(line):
                    position = Vector(x, y)
                    
                    if char == '-':
                        self.tracks.append(self.horizontal(position))
                    elif char == '|':
                        self.tracks.append(self.vertical(position))
                    elif char == '/':
                        if prior in ('-','+'):
                            connections = [
                                position + Vector(-1, 0),
                                position + Vector(0, -1),
                            ]
                        else:
                            connections = [
                                position + Vector(1, 0),
                                position + Vector(0, 1),
                            ]
                        
                        self.tracks.append(Corner(position, connections))
                    elif char == '\\':
                        if prior in ('-','+'):
                            connections = [
                                position + Vector(-1, 0),
                                position + Vector(0, 1),
                            ]
                        else:
                            connections = [
                                position + Vector(1, 0),
                                position + Vector(0, -1),
                            ]
                        
                        self.tracks.append(Corner(position, connections))
                    elif char == '+':
                        connections = [
                            position + Vector(1,0),
                            position + Vector(0,1),
                            position + Vector(-1,0),
                            position + Vector(0,-1),
                        ]
                        
                        self.tracks.append(Intersection(position, connections))
                    elif char == '<':
                        self.tracks.append(self.horizontal(position))
                        self.carts.append(Cart(position, Vector(-1,0)))
                    elif char == '>':
                        self.tracks.append(self.horizontal(position))
                        self.carts.append(Cart(position, Vector(1,0)))
                    elif char == '^':
                        self.tracks.append(self.vertical(position))
                        self.carts.append(Cart(position, Vector(0,-1)))
                    elif char == 'v':
                        self.tracks.append(self.vertical(position))
                        self.carts.append(Cart(position, Vector(0,1)))
                    # else: nothing
                    
                    prior = char
    
    def __iter__(self):
        yield self.tracks
        yield self.carts
    
    @classmethod
    def horizontal(cls, position):
        return Straightaway(position, [position + Vector(-1, 0), position + Vector(1, 0)])
    
    @classmethod
    def vertical(cls, position):
        return Straightaway(position, [position + Vector(0, -1), position + Vector(0, 1)])


def common_part(data, test):
    return TrackSystem(*(data or load('input/13.test' if test else 'input/13')))

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
    def __init__(self, tracks, carts):
        self.tracks = {x.position: x for x in tracks}
        self.carts = {x.position: x for x in carts}
        
        self.adopt(chain(self.tracks.values(), self.carts.values()))
    
    def __getitem__(self, key):
        return self.tracks.get(key)
    
    def __iter__(self):
        '''
        iterator for carts in proper order
        '''
        
        yield from sorted(self.carts.items(), key=lambda x: x[0])
    
    def adopt(self, orphans):
        for orphan in orphans:
            orphan.system = self
    
    def tick(self):
        for cart in self:
            cart.move()

class Track:
    def __init__(self, position, connections):
        self.position = position
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
    def __init__(self, position, connections):
        super().__init__(position)
        
        self.directions = tuple(x - self.position for x in self._connections)
    
    def next_direction(self, cart):
        return self.directions[1 - self.direction.index(cart.direction)]

class Intersection(Track):
    def next_direction(self, cart):
        return next(cart.intersection_direction)()

class Cart:
    def __init__(self, initial_position, initial_direction):
        self.position = initial_position
        self.direction = initial_direction
        self.intersection_direction = cycle([self.direction.counterclockwise, self.direction.copy, self.direction.clockwise])
    
    @property
    def track(self):
        return self.system.tracks[self.position]
    
    def move(self):
        #move forward one
        del self.system.carts[self.position]
        self.position += self.direction
        
        #did I crash?
        if self.position in self.system.carts:
            raise Crashed(self)
        else:
            self.system.carts[self.position] = self
        
        #turn according to the track landed on
        self.direction = self.track.next_direction(self)

class Crashed(Exception):
    def __init__(self, cart):
        self.cart = cart
        
        super().__init__()


if __name__=='__main__':
    run_as_script(
        part1,
        {load('input/13.test'): Vector(7,3)},
        part2,
        None
    )
