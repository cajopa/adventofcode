from collections import Counter


def load(input_filename):
    with open(input_filename, 'r') as f:
        for line in f:
            yield line.strip()

def part1():
    number_with_double = 0
    number_with_triple = 0
    
    for i in (Counter(x) for x in load('input/2')):
        if 2 in i.values():
            number_with_double += 1
        
        if 3 in i.values():
            number_with_triple += 1
    
    return number_with_double * number_with_triple

def part2():
    #trying to find the only two boxes whose IDs differ in only one position
    #use method of exclusion: can't have more than one difference
    
    data = list(load('input/2'))
    
    for i in data:
        for j in data:
            uncommon_positions = [x!=y for x,y in zip(i,j)]
            
            if sum(uncommon_positions) == 1:
                return ''.join(x for x,y in zip(i, uncommon_positions) if not y)
    
    raise Exception('No nearly-matching pairs in input.')
