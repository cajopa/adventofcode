import re
from itertools import chain, permutations


DEBUG=False
DEFAULT_INPUT='input/day13'
EXAMPLE_INPUT='input/day13.example'


def load(input_filename=DEFAULT_INPUT):
    with open(input_filename, 'r') as f:
        for line in (x.strip() for x in f):
            match = re.match(r'(?P<self>[A-Z][a-z]+) would (?P<gainlose>gain|lose) (?P<amount>\d+) happiness units by sitting next to (?P<other>[A-Z][a-z]+)\.', line)
            
            if match:
                sign = 1 if match.group('gainlose') == 'gain' else -1
                
                yield match.group('self'), sign*int(match.group('amount')), match.group('other')

def run1():
    indexed_conditions = index_conditions(load())
    
    return max((evaluate_seating_arrangement(x, indexed_conditions) for x in permutations(indexed_conditions.keys())))

def run2():
    indexed_conditions = index_conditions(load())
    
    for v in indexed_conditions.values():
        v['me'] = 0
    indexed_conditions['me'] = {k: 0 for k in indexed_conditions.keys()}
    
    return max((evaluate_seating_arrangement(x, indexed_conditions) for x in permutations(indexed_conditions.keys())))

def index_conditions(conditions):
    to_return = {}
    
    for self, amount, other in conditions:
        if self not in to_return:
            to_return[self] = {}
        
        to_return[self][other] = amount
    
    return to_return

def evaluate_seating_arrangement(arrangement, indexed_conditions):
    l = len(arrangement)
    clusters = [[arrangement[y] for y in x] for x in zip(range(-1,l), range(l), chain(range(1,l), [0]))]
    return sum((evaluate_happiness(self, left, right, indexed_conditions) for left,self,right in clusters))

def evaluate_happiness(self, left, right, indexed_conditions):
    return indexed_conditions[self][left] + indexed_conditions[self][right]
