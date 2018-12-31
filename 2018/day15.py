#!/usr/bin/env pypy3

from collections import defaultdict

from geometry import Vector
from util import run_as_script


DEBUG = False


class load:
    WALL = object()
    OPEN = object()
    ELF = object()
    GOB = object()
    
    
    def __init__(self, filename):
        with open(filename, 'r') as f:
            grid = self.parse(f)
        
        self.graph = self.mapify(grid)
    
    @classmethod
    def parse(cls, f):
        #parse input into basic grid with tokens
        grid = []
    
        for line in f:
            row = []
            
            for char in line:
                if char == '#':
                    row.append(cls.WALL)
                elif char == '.':
                    row.append(cls.OPEN)
                elif char == 'E':
                    row.append(cls.ELF)
                elif char == 'G':
                    row.append(cls.GOB)
            
            grid.append(row)
        
        return grid
    
    @classmethod
    def mapify(cls, grid):
        return Map(cls._mapify(grid))
    
    @classmethod
    def _mapify(cls, grid):
        for y,row in enumerate(grid):
            for x,item in enumerate(row):
                if not item is cls.WALL:
                    node = Open(Vector(x,y))
                    
                    if item is cls.ELF:
                        unit = Elf(node)
                    elif item is cls.GOB:
                        unit = Goblin(node)
                    
                    yield node

def part1(data=None):
    '''
    What is the outcome of the combat described in your puzzle input?
    '''

def part2(data=None):
    '''
    '''

'''
Map contains Open, Wall, Elf, Goblin
Per round, turns are taken per "reading order" (top to bottom, left to right)
Every Unit has 3 attack power and 200 initial HP
A turn is evaluate, optional move (early term if none valid), attack if possible
    Evaluate:
        identify all possible targets (end of game if none)
        "in range": orthogonally adjacent
        Determine if already "in range"
            if so, go to attack phase
            else, go to move phase
    Move:
        identify all Open "in range" of a target
        "step": single movement one orthogonally
        determine which "in range" Opens are closest in steps
            NOT manhattan distance (pathfinding)
        if multiple tied for closest, reading order (absolute) is preferred
        
        once destination determined, take one step toward it on a shortest path
            if multiple shortest paths, prefer reading order (absolute)
    Attack:
        determine all "in range" targets
        if none, end turn
        else,
            choose the target with fewest HP, prefer reading order
                reading order relative to self, so no right first, then down
            deal attack power damage
            if target's HP drops to 0 or below, dies
            on death, ceases to exist entirely (no map presence, no turns)
"outcome": [number of full rounds completed] * [sum of HP of all remaining units]
'''


class Map:
    def __init__(self, nodes=[]):
        self.nodes = set(nodes)
        
        self.adopt_nodes()
        self.link_nodes()
    
    def adopt(self, node):
        node.parent = self
    
    def adopt_nodes(self):
        for node in self.nodes:
            self.adopt(node)
    
    def link_nodes(self):
        indexed_nodes = defaultdict(lambda: None, ((x.position, x) for x in self.nodes))
        
        for node in self.nodes:
            node.link(indexed_nodes)

class Open:
    def __init__(self, position):
        self.position = position
        
        self.parent = None
        self.unit = None
        
        self.left = None
        self.right = None
        self.up = None
        self.down = None
    
    def link(self, indexed_nodes):
        self.left = indexed_nodes[self.position + Vector(-1,0)]
        self.right = indexed_nodes[self.position + Vector(1,0)]
        self.up = indexed_nodes[self.position + Vector(0,-1)]
        self.down = indexed_nodes[self.position + Vector(0,1)]

class Unit:
    def __init__(self, parent):
        self.parent = parent
        self.parent.unit = self
        
        self.hit_points = 200
        self.attack_power = 3
    
    @property
    def position(self):
        return self.parent.position
    
    def attack(self, other):
        other.take_damage(self.attack_power)
    
    def take_damage(self, amount):
        self.hit_points -= amount
        
        if self.hit_points <= 0:
            raise Died(self)

class Elf(Unit):
    pass

class Goblin(Unit):
    pass

class Died(Exception):
    def __init__(self, unit):
        self.unit = unit
        super().__init__()


if __name__=='__main__':
    run_as_script(15, part1, part2)
