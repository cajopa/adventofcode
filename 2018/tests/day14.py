import pytest

import day14


class Scoreboard:
    class CalculateDigits:
        def one_digit(self):
            assert day14.Scoreboard._calculate_digit_quantity(0) == 1
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
        
        def negative(self):
            assert day14.Scoreboard._calculate_digit_quantity(-1) == -1
            assert day14.Scoreboard._calculate_digit_quantity(-10) == -1
            assert day14.Scoreboard._calculate_digit_quantity(-100) == -1
    
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
        ])
        def multiple(self, start, stop, expected):
            fixture = day14.Scoreboard()
            fixture.scores = 3704836201
            
            assert fixture[start:stop] == expected

# @pytest.mark.parametrize('data,expected',[
#     (9, '5158916779'),
#     (5, '0124515891'),
#     (18, '9251071085'),
#     (2018, '5941429882'),
# ])
# def part1(data, expected):
#     assert day14.part1(data=data) == expected

class Part2():
    pass
