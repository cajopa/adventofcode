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
    
    class ExtractScore:
        def one_digit(self):
            fixture = day14.Scoreboard()
            fixture.scores = 4
            
            assert fixture._extract_score(0) == 4
        
        def two_digits(self):
            fixture = day14.Scoreboard()
            
            assert fixture._extract_score(0) == 3
            assert fixture._extract_score(1) == 7
        
        def ten_digits(self):
            fixture = day14.Scoreboard()
            fixture.scores = 3704836201
            
            assert fixture._extract_score(0) == 3
            assert fixture._extract_score(1) == 7
            assert fixture._extract_score(2) == 0
            assert fixture._extract_score(3) == 4
            assert fixture._extract_score(4) == 8
            assert fixture._extract_score(5) == 3
            assert fixture._extract_score(6) == 6
            assert fixture._extract_score(7) == 2
            assert fixture._extract_score(8) == 0
            assert fixture._extract_score(9) == 1

class Part1():
    pass

class Part2():
    pass
