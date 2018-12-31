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
        except (Genocide, NoTargets):
            return self.score(full_rounds)
    
    def score(self, full_rounds):
        return full_rounds * sum(x.unit.hit_points for x in self.nodes if x.unit)
    
    def has_genocide_occurred(self, dead_units=set()):
        all_units = set(x.unit for x in self.nodes if x.unit)
        live_units = all_units - dead_units
        
        return len({x.__class__ for x in live_units}) == 1

class Open:
    PathInfo = namedtuple('PathInfo', 'destination distance directions')
    
    
    def __init__(self, position):
        self.position = position
        
        self.parent = None
        self.unit = None
        
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        
        self.neighborhood = None
    
    def link(self, indexed_nodes):
        self.left = indexed_nodes[self.position + Vector(-1,0)]
        self.right = indexed_nodes[self.position + Vector(1,0)]
        self.up = indexed_nodes[self.position + Vector(0,-1)]
        self.down = indexed_nodes[self.position + Vector(0,1)]
        
        self.neighborhood = {self.left, self.right, self.up, self.down}
    
    def distance_to(self, other):
        return (self.position - other.position).rect_magnitude
    
    def find_shortest_path(self, destination, current_shortest, prefix=[], visited=set()):
        '''
        Uses recursive variation of A*, using manhattan distance as heuristic and pruning aid.
        
        .param.destination: type=Open
        .param.current_shortest: type=int
        .param.prefix: type=list(Node) #prior elements in the path
        .param.visited: type=set(Node) #nodes previously visited
        
        .return: type=PathInfo
        '''
        
        manhattan_distance = self.distance_to(destination)
        
        if manhattan_distance == 0:
            return cls.PathInfo(
                destination=destination,
                distance=len(prefix) + 1,
                directions=prefix + [destination]
            )
        elif not current_shortest or len(prefix) + manhattan_distance < current_shortest:
            if manhattan_distance == 1:
                return destination.find_shortest_path(
                    destination,
                    current_shortest,
                    prefix=prefix+[self],
                    visited=visited|{self}
                )
            else:
                prioritized_neighbors = sorted(self.neighborhood, key=lambda x: x.distance_to(destination))
                
                #FIXME: find multiple shortest paths and select the one where the first step is earlier in reading order
                
                for node in prioritized_neighbors:
                    exploratory_result = node.find_shortest_path(
                        destination,
                        current_shortest,
                        prefix=prefix+[self],
                        visited=visited|{self}
                    )
                    
                    if exploratory_result:
                        if isinstance(exploratory_result, set):
                            visited |= exploratory_result
                        else: #assume it's a PathInfo
                            return exploratory_result
        else:
            return visited | {self}

class Unit:
    IN_RANGE = object()
    
    
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
        '''
        
        evaluation = self.evaluate_phase()
        
        if evaluation is self.IN_RANGE:
            self.attack_phase()
        else:
            self.move_phase(evaluation)
    
    def evaluate_phase(self):
        '''
        Evaluate:
            identify all possible targets (end of game if none)
            "in range": orthogonally adjacent
            Determine if already "in range"
                if so, go to attack phase
                else, go to move phase
        '''
        
        in_range_targets = [x.unit for x in self.parent.neighborhood if x and x.unit]
        
        if in_range_targets:
            return self.IN_RANGE
        else:
            #find all potential targets
            return [x.unit for x in self.parent.parent.nodes if x.unit and not isinstance(x, self.__class__)]
    
    def move_phase(self, potential_targets):
        '''
        Move:
            identify all Open "in range" of a target
            "step": single movement one orthogonally
            determine which "in range" Opens are closest in steps
                NOT manhattan distance (pathfinding)
            if multiple tied for closest, reading order (absolute) is preferred
            
            once destination determined, take one step toward it on a shortest path
                if multiple shortest paths, prefer reading order (absolute)
        '''
        
        open_in_range_nodes = self._find_open_in_range(potential_targets)
        
        min_path = None
        
        for node in open_in_range_nodes:
            path = self.find_shortest_path(node, min_path and min_path.distance)
            
            if path and isinstance(path, PathInfo):
                min_path = path
    
    @classmethod
    def _find_open_in_range(cls, targets):
        for target in targets:
            yield from (node for node in target.neighborhood if node and not node.unit)
    
    def find_shortest_path(self, destination, current_shortest):
        '''
        Find shortest path from self to destination.
        '''
        
        return self.parent.find_shortest_path(destination, current_shortest)
    
    def attack_phase(self):
        '''
        Attack:
            determine all "in range" targets
            if none, end turn
            else,
                choose the target with fewest HP, prefer reading order (absolute)
                deal attack power damage
                if target's HP drops to 0 or below, dies
                on death, ceases to exist entirely (no map presence, no turns)
        '''
        
        target = min((x.unit for x in self.parent.neighborhood if x and x.unit), key=lambda x: (x.hit_points, x.position))
        
        self.attack(target)

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

class NoTargets(Exception):
    pass


if __name__=='__main__':
    run_as_script(15, part1, part2)
