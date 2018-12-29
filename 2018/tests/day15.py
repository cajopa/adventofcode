import os

import pytest

import day15


def _readall():
    base_dir = 'input/15.test'
    
    for filename in os.listdir(base_dir):
        with open(base_dir + '/' + filename, 'r') as f:
            yield f.read()

class load:
    def parse(self):
        data = ['###\n','.EG\n']
        expected = [
            [day15.load.WALL] * 3,
            [day15.load.OPEN, day15.load.ELF, day15.load.GOB]
        ]
        
        assert day15.load.parse(data) == expected

# @pytest.mark.parametrize('data,expected',zip(
#     _readall(),
#     [
#         27730,
#         36334,
#         39514,
#         27755,
#         28944,
#         18740,
#     ]
# ))
# def part1(data, expected):
#     assert day15.part1(data) == expected

# @pytest.mark.parametrize('data,expected',[
# ])
# def part2(data, expected):
#     pass
