import json
import re
import sys
from collections import Mapping, Sequence


if sys.version_info.major < 3:
    raise ImportError('requires Python 3')


DEBUG=False


def run1(input_filename='input/day12'):
    with open(input_filename, 'r') as f:
        return sum(map(int, re.findall(r'\-?\d+', f.read())))

def run2(input_filename='input/day12'):
    with open(input_filename, 'r') as f:
        data = json.load(f)
    
    return sum((x for x in walk(data, lambda x: x=='red') if isinstance(x, int)))

def walk(root, prune_condition=lambda x: False):
    #can be either a list or a dict
    
    if DEBUG:
        print('walking into {}'.format(root))
    
    if isinstance(root, Sequence) and not isinstance(root, str):
        if DEBUG:
            print('is sequence: descending')
        
        for i in root:
            yield from walk(i, prune_condition)
    elif isinstance(root, Mapping):
        if DEBUG:
            print('is mapping: ', end='')
        
        if any((prune_condition(v) for v in root.values())):
            if DEBUG:
                print('pruning')
            
            yield None
        else:
            if DEBUG:
                print('descending')
            
            for v in root.values():
                yield from walk(v, prune_condition)
    else:
        if DEBUG:
            print('is non-collection: yielding')
        
        yield root
