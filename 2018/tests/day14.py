import pytest

import day14


class Scoreboard:
    class CalculateDigits:
        def one_digit(self):
            assert day14.Scoreboard._calculate_digit_quantity(1) == 1
            assert day14.Scoreboard._calculate_digit_quantity(2) == 1
            assert day14.Scoreboard._calculate_digit_quantity(3) == 1
            assert day14.Scoreboard._calculate_digit_quantity(9) == 1
        
        def two_digits(self):
            assert day14.Scoreboard._calculate_digit_quantity(10) == 2
            assert day14.Scoreboard._calculate_digit_quantity(11) == 2
            assert day14.Scoreboard._calculate_digit_quantity(12) == 2
            assert day14.Scoreboard._calculate_digit_quantity(13) == 2
            assert day14.Scoreboard._calculate_digit_quantity(19) == 2
        
        def fifty_digits(self):
            assert day14.Scoreboard._calculate_digit_quantity(10**49 + 0) == 50
            assert day14.Scoreboard._calculate_digit_quantity(10**49 + 1) == 50
            assert day14.Scoreboard._calculate_digit_quantity(10**49 + 2) == 50
            assert day14.Scoreboard._calculate_digit_quantity(10**49 + 3) == 50
            assert day14.Scoreboard._calculate_digit_quantity(10**49 + 9) == 50
    
    class getitem:
        def one_digit(self):
            fixture = day14.Scoreboard()
            fixture.scores = 4
            
            assert fixture[0] == 4
        
        def two_digits(self):
            fixture = day14.Scoreboard()
            
            assert fixture[0] == 3
            assert fixture[1] == 7
        
        def ten_digits(self):
            fixture = day14.Scoreboard()
            fixture.scores = 3704836201
            
            assert fixture[0] == 3
            assert fixture[1] == 7
            assert fixture[2] == 0
            assert fixture[3] == 4
            assert fixture[4] == 8
            assert fixture[5] == 3
            assert fixture[6] == 6
            assert fixture[7] == 2
            assert fixture[8] == 0
            assert fixture[9] == 1
        
        @pytest.mark.parametrize('start,stop,expected', [
            (0, 2, 37),
            (0, -1, 370483620),
            (0, None, 3704836201),
            (-2, -1, 0),
            (-2, None, 1),
            (2,4,4),
            (9,None,1),
        ])
        def multiple(self, start, stop, expected):
            fixture = day14.Scoreboard()
            fixture.scores = 3704836201
            
            assert fixture[start:stop] == expected
    
    @pytest.mark.parametrize('loop_quantity,scores,positions', [
        (1, 3710, (0,1)),
        (2, 371010, (4,3)),
        (3, 3710101, (6,4)),
        (4, 37101012, (0,6)),
        (5, 371010124, (4,8)),
        (6, 3710101245, (6,3)),
        (7, 37101012451, (8,4)),
        (8, 371010124515, (1,6)),
        (9, 3710101245158, (9,8)),
        (10, 37101012451589, (1,13)),
        (11, 3710101245158916, (9,7)),
        (12, 37101012451589167, (15,10)),
        (13, 371010124515891677, (4,12)),
        (14, 3710101245158916779, (6,2)),
        (15, 37101012451589167792, (8,4)),
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
        
        assert len(fixture) >= length

@pytest.mark.parametrize('data,expected',[
    (9, '5158916779'),
    (5, '0124515891'),
    (18, '9251071085'),
    (2018, '5941429882'),
])
def part1(data, expected):
    assert day14.part1(data=data) == expected

class Part2():
    pass
