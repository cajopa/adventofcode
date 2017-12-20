from itertools import izip, islice


FACTOR_A = 16807
FACTOR_B = 48271
DIVISOR = 2147483647
MULTIPLE_A = 4
MULTIPLE_B = 8

START_A = 618
START_B = 814


def run1(start_a=START_A, factor_a=FACTOR_A, start_b=START_B, factor_b=FACTOR_B, divisor=DIVISOR, rounds=40000000):
    generator_a = generator(start_a, factor_a, divisor)
    generator_b = generator(start_b, factor_b, divisor)
    
    return count_matches(generator_a, generator_b, rounds)
    
    return len([None for x in islice(izip(generator(start_a, factor_a, divisor), generator(start_b, factor_b, divisor)), rounds) if (x[0] ^ x[1]) & 0xffff == 0])

def run2(start_a=START_A, factor_a=FACTOR_A, start_b=START_B, factor_b=FACTOR_B, divisor=DIVISOR, rounds=5000000):
    generator_a = generator(start_a, factor_a, divisor, multiple_of=MULTIPLE_A)
    generator_b = generator(start_b, factor_b, divisor, multiple_of=MULTIPLE_B)
    
    return count_matches(generator_a, generator_b, rounds)

def count_matches(generator_a, generator_b, rounds):
    return len([None for x in islice(izip(generator_a, generator_b), rounds) if (x[0] ^ x[1]) & 0xffff == 0])

def generator(start, factor, divisor, multiple_of=1):
    current = start
    
    while True:
        current = current * factor % divisor
        
        if current % multiple_of == 0:
            yield current
