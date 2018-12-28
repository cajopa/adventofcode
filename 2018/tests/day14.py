import pytest

import day14


class Scoreboard:
    @pytest.mark.parametrize('loop_quantity,scores,positions', [
        (0, [3,7], (0,1)),
        (1, [3,7,1,0], (0,1)),
        (2, [3,7,1,0,1,0], (4,3)),
        (3, [3,7,1,0,1,0,1], (6,4)),
        (4, [3,7,1,0,1,0,1,2], (0,6)),
        (5, [3,7,1,0,1,0,1,2,4], (4,8)),
        (6, [3,7,1,0,1,0,1,2,4,5], (6,3)),
        (7, [3,7,1,0,1,0,1,2,4,5,1], (8,4)),
        (8, [3,7,1,0,1,0,1,2,4,5,1,5], (1,6)),
        (9, [3,7,1,0,1,0,1,2,4,5,1,5,8], (9,8)),
        (10, [3,7,1,0,1,0,1,2,4,5,1,5,8,9], (1,13)),
        (11, [3,7,1,0,1,0,1,2,4,5,1,5,8,9,1,6], (9,7)),
        (12, [3,7,1,0,1,0,1,2,4,5,1,5,8,9,1,6,7], (15,10)),
        (13, [3,7,1,0,1,0,1,2,4,5,1,5,8,9,1,6,7,7], (4,12)),
        (14, [3,7,1,0,1,0,1,2,4,5,1,5,8,9,1,6,7,7,9], (6,2)),
        (15, [3,7,1,0,1,0,1,2,4,5,1,5,8,9,1,6,7,7,9,2], (8,4)),
    ])
    def increment(self, loop_quantity, scores, positions):
        fixture = day14.Scoreboard()
        
        for _ in range(loop_quantity):
            fixture.increment()
        
        assert fixture.scores == scores
        assert fixture.positions == positions
    
    @pytest.mark.parametrize('length', [
        1,
        2,
        5,
        10,
        1000,
    ])
    def run_until_length(self, length):
        fixture = day14.Scoreboard()
        
        fixture.run_until_length(length)
        
        assert len(fixture.scores) >= length

@pytest.mark.parametrize('data,expected',[
    (9, '5158916779'),
    (5, '0124515891'),
    (18, '9251071085'),
    (2018, '5941429882'),
])
def part1(data, expected):
    assert day14.part1(data=data) == expected

@pytest.mark.parametrize('data,expected',[
    ([5,1,5,8,9], 9),
    ([0,1,2,4,5], 5),
    ([9,2,5,1,0], 18),
    ([5,9,4,1,4], 2018),
])
def part2(data, expected):
    assert day14.part2(data=data) == expected
