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
                        Elf(node)
                    elif item is cls.GOB:
                        Goblin(node)
                    
                    yield node

def part1(data=None):
    '''
    What is the outcome of the combat described in your puzzle input?
    '''
    
    graph = load(data or 'input/15').graph
    
    return graph.run_until_genocide()

def part2(data=None):
    '''
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
    
    def run_round(self):
        #positions of units will likely change during the round, so save order now
        units_in_order = list(sorted((x.unit for x in self.nodes if x.unit), key=lambda x: x.position))
        dead_units = set()
        
        for unit in units_in_order:
            if self.has_genocide_occurred(dead_units):
                raise Genocide
            
            if unit not in dead_units:
                try:
                    unit.take_turn()
                except Died as e:
                    dead_units.add(e.unit)
        else:
            raise Exception('no units left on the map!')
    
    def run_until_genocide(self):
        full_rounds = 0
        
        try:
            while True:
                self.run_round()
                full_rounds += 1
        except Genocide:
            return self.score(full_rounds)
    
    def score(self, full_rounds):
        return full_rounds * sum(x.unit.hit_points for x in self.nodes if x.unit)
    
    def has_genocide_occurred(self, dead_units=set()):
        all_units = set(x.unit for x in self.nodes if x.unit)
        live_units = all_units - dead_units
        
        return len({x.__class__ for x in live_units}) == 1

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
            self.parent.unit = None
            
            raise Died(self)
    
    def take_turn(self):
        '''
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
        '''

class Elf(Unit):
    pass

class Goblin(Unit):
    pass

class Died(Exception):
    def __init__(self, unit):
        self.unit = unit
        super().__init__()

class Genocide(Exception):
    pass


if __name__=='__main__':
    run_as_script(15, part1, part2)
