import re


DEBUG = False

DEFAULT_INPUT = 'input/day16.sues'

PACKAGE_TRAITS = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}


def load(input_filename=DEFAULT_INPUT):
    with open(input_filename, 'r') as f:
        for line in (x.strip() for x in f):
            match = re.match(r'Sue (?P<number>\d+): (?P<traits>.*)', line)
            
            if match:
                sue_number = int(match.group('number'))
                
                traits = {k: int(v) for k,v in (x.split(': ') for x in match.group('traits').split(', '))}
                
                yield sue_number, traits

def run1():
    return [sue_number for sue_number, traits in load() if match_sue(traits)]

def run2():
    return [sue_number for sue_number, traits in load() if fuzzy_match_sue(traits)]

def match_sue(traits):
    return all(PACKAGE_TRAITS[name] == value for name, value in traits.items())

def fuzzy_match_sue(traits):
    def inner():
        for name, value in traits.items():
            if name in ('cats', 'trees'):
                yield value > PACKAGE_TRAITS[name]
            elif name in ('pomeranians', 'goldfish'):
                yield value < PACKAGE_TRAITS[name]
            else:
                yield value == PACKAGE_TRAITS[name]
    
    return all(inner())
