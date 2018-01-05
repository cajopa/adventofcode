import re
import itertools


DEBUG = False


def load(input_filename='input/day09'):
    with open(input_filename, 'r') as f:
        for line in (x.strip() for x in f):
            match = re.match(r'(?P<from>[a-zA-Z]+) to (?P<to>[a-zA-Z]+) = (?P<distance>\d+)', line)
            
            yield match.group('from'), match.group('to'), int(match.group('distance'))

def run1():
    return min(find_lengths(), key=lambda x: x[0])

def run2():
    return max(find_lengths(), key=lambda x: x[0])

def find_lengths(raw_paths=None):
    if not raw_paths:
        raw_paths = list(load())
    
    paths = {(x[0], x[1]): x[2] for x in raw_paths}
    paths.update({(x[1], x[0]): x[2] for x in raw_paths})
    nodes = set((x[0] for x in paths)) | set((x[1] for x in paths))
    
    for total_path in itertools.permutations(nodes):
        if all(((a,b) in paths for a,b in zip(total_path, total_path[1:]))):
            yield sum((paths[(a,b)] for a,b in zip(total_path, total_path[1:]))), total_path
