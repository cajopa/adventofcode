import itertools


def minmaxcksum(rows):
    return sum((max(row) - min(row) for row in rows))

def divmodsum(rows):
    def inner(row):
        for a,b in itertools.combinations(sorted(row), 2):
            d,m = divmod(b, a)
            
            if m == 0:
                return d
    
    return sum(map(inner, rows))

def process_input(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield [int(x) for x in line.split(' ') if x]
