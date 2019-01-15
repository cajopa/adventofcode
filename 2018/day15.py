#!/usr/bin/env pypy3

from collections import defaultdict, namedtuple
from functools import reduce

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
                    node = Node(Vector(x,y))
                    
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
    
    def __str__(self):
        max_x = max(x.position.x for x in self.nodes)
        max_y = max(x.position.y for x in self.nodes)
        
        indexed_nodes = self.indexed_nodes
        
        def inner():
            for y in range(max_y + 1):
                for x in range(max_x + 1):
                    node = indexed_nodes[Vector(x,y)]
                    
                    if node:
                        if node.unit:
                            if isinstance(node.unit, Elf):
                                yield 'E'
                            elif isinstance(node.unit, Goblin):
                                yield 'G'
                        else:
                            yield '\u00b7'
                    else:
                        yield '\u2588'
                
                yield '\n'
        
        return ''.join(inner())
    
    @property
    def indexed_nodes(self):
        return defaultdict(lambda: None, ((x.position, x) for x in self.nodes))
    
    def adopt(self, node):
        node.parent = self
    
    def adopt_nodes(self):
        for node in self.nodes:
            self.adopt(node)
    
    def link_nodes(self):
        indexed_nodes = self.indexed_nodes
        
        for node in self.nodes:
            node.link(indexed_nodes)
    
    def run_round(self):
        #positions of units will likely change during the round, so save order now
        units_in_order = list(sorted((x.unit for x in self.nodes if x.unit), key=lambda x: tuple(reversed(tuple(x.position)))))
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
            raise NoTargets
        
        print(self)
        print(' '.join(map(str, (x.unit.hit_points for x in self.nodes if x.unit))))
    
    def run_until_genocide(self):
        full_rounds = 0
        
        try:
            while True:
                self.run_round()
                full_rounds += 1
        except (Genocide, NoTargets):
            print(f'full rounds: {full_rounds}')
            return self.score(full_rounds)
    
    def score(self, full_rounds):
        return full_rounds * sum(x.unit.hit_points for x in self.nodes if x.unit)
    
    def has_genocide_occurred(self, dead_units=set()):
        all_units = set(x.unit for x in self.nodes if x.unit)
        live_units = all_units - dead_units
        
        return len({x.__class__ for x in live_units}) == 1

class Node:
    PathInfo = namedtuple('PathInfo', 'destination distance directions')
    
    
    def __init__(self, position):
        self.position = position
        
        self.parent = None
        self.unit = None
        
        self.neighborhood = None
    
    def __repr__(self):
        if self.unit:
            return f'<{self.__class__.__name__} @{self.position} ({self.unit})>'
        else:
            return f'<{self.__class__.__name__} @{self.position}>'
    
    def __lt__(self, other):
        return tuple(reversed(tuple(self.position))) < tuple(reversed(tuple(self.position)))
    
    def link(self, indexed_nodes):
        left = indexed_nodes[self.position + Vector(-1,0)]
        right = indexed_nodes[self.position + Vector(1,0)]
        up = indexed_nodes[self.position + Vector(0,-1)]
        down = indexed_nodes[self.position + Vector(0,1)]
        
        self.neighborhood = {left, right, up, down} - {None}
    
    def distance_to(self, other):
        return (self.position - other.position).rect_magnitude
    
    def find_shortest_paths(self, destination, target_length, prefix=[]):
        '''
        Uses recursive variation of A*, using manhattan distance as heuristic and pruning aid.
        
        .param.destination: type=Node
        .param.target_length: type=int
        .param.prefix: type=list(Node) #prior elements in the path
        
        .return: type=list(PathInfo)
        '''
        
        manhattan_distance = self.distance_to(destination)
        
        if DEBUG:
            def inprint(indent, message):
                indent_str = ' ' * (4 + 6*len(prefix) + 2*indent)
                print(indent_str + message)
            
            inprint(0, f'FSPs: src={self} dest={destination} c_s={target_length} pre={prefix}')
            inprint(1, f'dist={manhattan_distance}')
        
        if manhattan_distance == 0:
            if DEBUG:
                inprint(1, 'returning PathInfo')
            
            return [self.PathInfo(
                destination=destination,
                distance=len(prefix),
                directions=prefix
            )]
        elif target_length is None or len(prefix) + manhattan_distance < target_length:
            if DEBUG:
                inprint(1, 'reachable')
            
            if manhattan_distance == 1:
                if DEBUG:
                    inprint(2, 'in range')
                
                return destination.find_shortest_paths(
                    destination,
                    target_length,
                    prefix=prefix+[destination],
                )
            else:
                prioritized_neighbors = sorted(self.neighborhood - set(prefix), key=lambda x: x.distance_to(destination))
                
                if DEBUG:
                    inprint(2, 'out of range')
                    inprint(3, f'prioritized_neighbors={prioritized_neighbors}')
                
                shortest_paths = []
                
                for node in prioritized_neighbors:
                    exploratory_results = node.find_shortest_paths(
                        destination,
                        target_length,
                        prefix=prefix+[node],
                    )
                    
                    if DEBUG:
                        inprint(4, f'exploratory_results={exploratory_results}')
                    
                    if exploratory_results:
                        min_distance = min(x.distance for x in exploratory_results)
                        
                        if target_length is None or min_distance < target_length:
                            if DEBUG:
                                inprint(5, 'replacing shortest path(s)')
                            
                            target_length = min_distance
                            shortest_paths = [x for x in exploratory_results if x.distance == min_distance]
                        elif min_distance == target_length:
                            if DEBUG:
                                inprint(5, 'extending shortest path(s)')
                            
                            shortest_paths.extend(x for x in exploratory_results if x.distance == min_distance)
                        else:
                            if DEBUG:
                                inprint(5, 'discarding new paths')
                    else:
                        if DEBUG:
                            inprint(5, 'no new paths')
                
                if shortest_paths:
                    if DEBUG:
                        inprint(2, f'returning paths: {shortest_paths}')
                else:
                    if DEBUG:
                        inprint(2, 'no shortest paths')
                
                return shortest_paths
        else:
            if DEBUG:
                inprint(1, 'drifted too far')
            
            return []

class Unit:
    IN_RANGE = object()
    
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.unit = self
        
        self.hit_points = 200
        self.attack_power = 3
    
    def __repr__(self):
        return f'<{self.__class__.__name__} HP:{self.hit_points}/200>'
    
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
    
    def move(self, node):
        self.parent = node
        self.parent.unit = self
    
    def take_turn(self):
        '''
        A turn is:
          - evaluate
          - attack if possible (ends turn)
          - move if possible (ends turn if impossible)
          - attack if possible (ends turn)
        '''
        
        if DEBUG:
            print(f'taking turn: {self}')
        
        try:
            attackable_nodes = self.evaluate_phase()
        except CanAttackNow:
            self.attack_phase()
        else:
            try:
                self.move_phase(attackable_nodes)
            except CanAttackNow:
                self.attack_phase()
        
        if DEBUG:
            print('  # END OF TURN #')
    
    def evaluate_phase(self):
        '''
        Evaluate:
            identify all possible targets (end of turn if none)
            "in range": orthogonally adjacent
            Determine if already "in range"
                if so, go to attack phase
                else, go to move phase
        '''
        
        if DEBUG:
            print('  EVALUATE PHASE')
        
        in_range_targets = [x.unit for x in self.parent.neighborhood if x.unit and not isinstance(x.unit, self.__class__)]
        
        if any(True for x in self.parent.neighborhood if x.unit and not isinstance(x.unit, self.__class__)):
            if DEBUG:
                print('    in range')
            
            raise CanAttackNow
        else:
            if DEBUG:
                to_return = [x for x in self.parent.parent.nodes if x.unit and not isinstance(x.unit, self.__class__)]
                
                print(f'    potential targets: {to_return}')
                
                return to_return
            else:
                #find all potential targets
                return [x for x in self.parent.parent.nodes if x.unit and not isinstance(x.unit, self.__class__)]
        
        if DEBUG:
            print('    = END OF PHASE =')
    
    def move_phase(self, attackable_nodes):
        '''
        Move:
            identify all Node "in range" of a target
            "step": single movement one orthogonally
            determine which "in range" Opens are closest in steps
                NOT manhattan distance (pathfinding)
            if multiple tied for closest, reading order (absolute) is preferred
            
            once destination determined, take one step toward it on a shortest path
                if multiple shortest paths, prefer reading order (absolute)
        '''
        
        if DEBUG:
            print('  MOVE PHASE')
        
        open_in_range_nodes = self._find_open_in_range(attackable_nodes)
        
        if DEBUG:
            print(f'    open and in range: {open_in_range_nodes}')
        
        try:
            first_destination = next(open_in_range_nodes)
        except StopIteration:
            if DEBUG:
                print('    cannot move')
            
            raise CannotMove
        
        min_path = self.find_shortest_path(first_destination, None)
        
        for node in open_in_range_nodes:
            path = self.find_shortest_path(node, min_path and min_path.distance)
            
            if not min_path or (path and path.distance < min_path.distance):
                min_path = path
        
        if DEBUG:
            print(f'    min_path: {min_path}')
            print(f'    moving to {min_path[0]}')
        
        self.move(min_path[0])
        
        print('    = END OF PHASE =')
    
    @classmethod
    def _find_open_in_range(cls, targets):
        for target in targets:
            yield from (node for node in target.neighborhood if not node.unit)
    
    def find_shortest_path(self, destination, current_shortest):
        '''
        Find shortest path from self to destination.
        
        If there are multiple shortest paths, select the one where the first step is earlier in reading order.
        '''
        
        shortest_paths = self.parent.find_shortest_paths(destination, current_shortest)
        
        if not shortest_paths:
            if DEBUG:
                print('no shortest paths: cannot move')
            
            return None
        
        if DEBUG:
            print(f'shortest paths from {self}@{self.position} to {destination}: {shortest_paths}')
        
        if shortest_paths:
            return min(shortest_paths, key=lambda x: x.directions)
    
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
        
        if DEBUG:
            print('  ATTACK PHASE')
        
        target = min((x.unit for x in self.parent.neighborhood if x.unit), key=lambda x: (x.hit_points, tuple(reversed(tuple(x.position)))))
        
        if DEBUG:
            print(f'    attacking {target}@{target.position}')
        
        self.attack(target)
        
        if DEBUG:
            print('    = END OF PHASE =')

class Elf(Unit):
    pass

class Goblin(Unit):
    pass

class Died(Exception):
    def __init__(self, unit):
        self.unit = unit
        super().__init__()

class Genocide(Exception): pass

class NoTargets(Exception): pass

class CanAttackNow(Exception): pass

class CannotMove(Exception): pass


if __name__=='__main__':
    run_as_script(15, part1, part2)
