#!/usr/bin/env pypy3

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
        
        self.graph = self.graphify(grid)
    
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
    def graphify(cls, grid):
        #convert tokens to nodes/units
        #hook up objects to each other for later traversal
        pass

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


if __name__=='__main__':
    run_as_script(15, part1, part2)
