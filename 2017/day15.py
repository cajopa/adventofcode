from itertools import izip, islice


FACTOR_A = 16807
FACTOR_B = 48271
DIVISOR = 2147483647

START_A = 618
START_B = 814


def run1(start_a=START_A, factor_a=FACTOR_A, start_b=START_B, factor_b=FACTOR_B, divisor=DIVISOR, rounds=40000000):
    return len([None for x in islice(izip(generator(start_a, factor_a, divisor), generator(start_b, factor_b, divisor)), rounds) if (x[0] ^ x[1]) & 0xffff == 0])

def generator(start, factor, divisor):
    current = start
    
    while True:
        current = current * factor % divisor
        yield current
