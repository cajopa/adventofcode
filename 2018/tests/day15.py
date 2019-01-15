import os

import pytest

from geometry import Vector
import day15


def _findall():
    base_dir = 'input/15.test'
    
    for filename in os.listdir(base_dir):
        yield base_dir + '/' + filename

class load:
    def parse(self):
        data = ['###\n','.EG\n']
        expected = [
            [day15.load.WALL] * 3,
            [day15.load.OPEN, day15.load.ELF, day15.load.GOB]
        ]
        
        assert day15.load.parse(data) == expected
    
    def under_mapify(self):
        data = [
            [day15.load.WALL] * 3,
            [day15.load.OPEN, day15.load.ELF, day15.load.GOB]
        ]
        
        inodes = day15.load._mapify(data)
        
        node = next(inodes)
        assert isinstance(node, day15.Node)
        assert not node.unit
        assert node.position == Vector(0,1)
        
        node = next(inodes)
        assert isinstance(node, day15.Node)
        assert isinstance(node.unit, day15.Elf)
        assert node.position == Vector(1,1)
        
        node = next(inodes)
        assert isinstance(node, day15.Node)
        assert isinstance(node.unit, day15.Goblin)
        assert node.position == Vector(2,1)

class Map:
    @pytest.mark.parametrize('rounds,hit_pointses,expected', [
        (47, [200,131,59,200], 27730),
        (37, [200,197,185,200,200], 36334),
        (46, [164,197,200,98,200], 39514),
        (35, [200,98,200,95,200], 27755),
        (54, [200,98,38,200], 28944),
        (20, [137,200,200,200,200], 18740),
    ])
    def score(self, rounds, hit_pointses, expected):
        def inner():
            for i,hp in enumerate(hit_pointses):
                node = day15.Node(Vector(i,0))
                unit = day15.Unit(node)
                unit.hit_points = hp
                
                yield node
        
        fixture = day15.Map(inner())
        
        assert fixture.score(rounds) == expected
    
    @pytest.mark.parametrize('unit_map,dead_unit_map,expected', [
        ('E', set(), True),
        ('EE', {1,}, True,),
        ('EG', {1,}, True),
        ('EE', set(), True),
        ('EEG', {2,}, True),
        ('EEE', {2,}, True),
        ('EG', set(), False),
        ('EGG', {1,}, False),
        ('EGG', {0,}, True),
    ])
    def has_genocide_occurred(self, unit_map, dead_unit_map, expected):
        nodes = []
        dead_units = set()
        
        for i,x in enumerate(unit_map):
            nodes.append(day15.Node(Vector(i, 0)))
            
            if x == 'E':
                unit = day15.Elf(nodes[-1])
            elif x == 'G':
                unit = day15.Goblin(nodes[-1])
            
            if i in dead_unit_map:
                dead_units.add(unit)
        
        fixture = day15.Map(nodes)
        
        assert fixture.has_genocide_occurred(dead_units) == expected

class Node:
    class find_shortest_paths:
        def finds_shortest(self):
            pass
        
        def prefers_reading_order(self):
            pass
        
        def finds_all_shortest(self):
            pass

class Unit:
    '''
    take_damage
    evaluate_phase
    _find_open_in_range
    find_shortest_path
    _shorter_path
    
    need mock objects and ability to check that an exception occurred
    '''

@pytest.mark.parametrize('data,expected',zip(
    _findall(),
    [
        27730,
        36334,
        39514,
        27755,
        28944,
        18740,
    ]
))
def part1(data, expected):
    assert day15.part1(data) == expected

# @pytest.mark.parametrize('data,expected',[
# ])
# def part2(data, expected):
#     pass
