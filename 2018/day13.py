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
                        if prior in ('-','+','<','>'):
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
                        if prior in ('-','+','<','>'):
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


def common_part(data):
    return TrackSystem(*(data or load('input/13')))

def part1(data=None, test=False):
    '''
    After following their respective paths for a while, the carts eventually crash. To help prevent
    crashes, you'd like to know the location of the first crash. Locations are given in X,Y
    coordinates, where the furthest left column is X=0 and the furthest top row is Y=0.
    '''
    
    try:
        common_part(data or test and load('input/13.1.test')).run_until_crash()
    except Crashed as e:
        return e.cart.position

def part2(data=None, test=None):
    '''
    What is the location of the last cart at the end of the first tick where it is the only cart left?
    '''
    
    return common_part(data or test and load('input/13.2.test')).run_until_highlander().position


class TrackSystem:
    def __init__(self, tracks, carts):
        self.tracks = {x.position: x for x in tracks}
        self.carts = {x.position: x for x in carts}
        
        self.adopt(chain(self.tracks.values(), self.carts.values()))
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {len(self.tracks)} tracks, {len(self.carts)} carts>'
    
    def __str__(self):
        max_x = max(x.x for x in self.tracks.keys())
        max_y = max(x.y for x in self.tracks.keys())
        
        def _inner():
            for y in range(max_y + 1):
                for x in range(max_x + 1):
                    position = Vector(x,y)
                    thing = self.carts.get(position) or self.tracks.get(position)
                    
                    if thing:
                        yield str(thing)
                    else:
                        yield ' '
                
                yield '\n'
        
        return ''.join(_inner())
    
    def __iter__(self):
        '''
        iterator for carts in proper order
        '''
        
        yield from sorted(self.carts.values(), key=lambda x: (x.position.y, x.position.x))
    
    def adopt(self, orphans):
        for orphan in orphans:
            orphan.system = self
    
    def tick(self):
        for cart in self:
            cart.move()
    
    def run_until_crash(self):
        while True:
            self.tick()
    
    def run_until_highlander(self):
        while len(self.carts) > 1:
            crashed_carts = set()
            
            for cart in self:
                try:
                    ### NOTE: can't use run_until_crash or even tick because we need to resume
                    #         from within the tick when a crash occurs
                    
                    cart.move()
                except Crashed as e:
                    #the crashed cart has already been removed from the index
                    #save for later and soft-skip in the meantime because we're iterating on self.carts
                    crashed_cart = self.carts[e.cart.position]
                    
                    crashed_cart.broken = True
                    crashed_carts.add(crashed_cart)
            
            for cart in crashed_carts:
                del self.carts[cart.position]
        
        return next(iter(self.carts.values()))

class Track:
    def __init__(self, position, connections):
        self.position = position
        self._connection_positions = connections
        
        self.system = None
    
    def __repr__(self):
        return f'<{self.__class__.__name__} pos:{self.position} conn:{self._connection_positions}>'
    
    def __str__(self):
        raise NotImplementedError
    
    @property
    def connections(self):
        return [self.system.tracks[x] for x in self._connection_positions]
    
    def next_direction(self, cart):
        raise NotImplementedError

class Straightaway(Track):
    def __str__(self):
        if abs((self._connection_positions[0] - self.position).x) == 1:
            return '-'
        else:
            return '|'
    
    def next_direction(self, cart):
        return cart.direction

class Corner(Track):
    def __init__(self, position, connections):
        super().__init__(position, connections)
        
        self.directions = tuple(x - self.position for x in self._connection_positions)
    
    def __str__(self):
        if (self._connection_positions[0] - self.position).x == (self._connection_positions[1] - self.position).y:
            return '/'
        else:
            return '\\'
    
    def next_direction(self, cart):
        return self.directions[1 - self.directions.index(-1 * cart.direction)]

class Intersection(Track):
    def __str__(self):
        return '+'
    
    def next_direction(self, cart):
        return next(cart.intersection_direction)()

class Cart:
    def __init__(self, initial_position, initial_direction):
        self.position = initial_position
        self.direction = initial_direction
        self.broken = False
        
        ### NOTE: Vector assumes upward is +y, but computer graphics conventions map downward to +y, so the winding function is reversed
        self.intersection_direction = cycle([lambda: self.direction.clockwise, lambda: self.direction, lambda: self.direction.counterclockwise])
    
    def __repr__(self):
        return f'<{self.__class__.__name__} pos:{self.position} dir:{self.direction}>'
    
    def __str__(self):
        if self.direction == Vector(1,0):
            return '=' if self.broken else '>'
        elif self.direction == Vector(-1,0):
            return '=' if self.broken else '<'
        elif self.direction == Vector(0,1):
            return '¦' if self.broken else 'v'
        elif self.direction == Vector(0,-1):
            return '¦' if self.broken else '^'
    
    @property
    def track(self):
        return self.system.tracks[self.position]
    
    def move(self):
        if not self.broken:
            #move forward one
            del self.system.carts[self.position]
            self.position += self.direction
            
            #did I crash?
            crashed_into_cart = self.system.carts.get(self.position)
            
            if crashed_into_cart and not crashed_into_cart.broken:
                raise Crashed(self)
            else:
                self.system.carts[self.position] = self
            
            #turn according to the track landed on
            self.direction = self.track.next_direction(self)

class Crashed(Exception):
    def __init__(self, cart):
        self.cart = cart
        
        super().__init__(f'at {cart.position}')


if __name__=='__main__':
    run_as_script(13)
