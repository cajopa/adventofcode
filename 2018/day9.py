#!/usr/bin/env python

import re


TEST_DATA = {
    (9,25): 32,
    (10,1618): 8317,
    (13,7999): 146373,
    (17,1104): 2764,
    (21,6111): 54718,
    (30,5807): 37305,
}


def load(input_filename):
    with open(input_filename, 'r') as f:
        #432 players; last marble is worth 71019 points
        match = re.match(r'(?P<players>\d+) players; last marble is worth (?P<maxpoints>\d+) points', f.read().strip())
        
        return int(match.group('players')), int(match.group('maxpoints'))

def common_part(data=None, test=None):
    data = data or (load('input/9') if test is None else TEST_DATA[test])
    
    pass

def part1(data=None, test=None):
    '''
    '''
    
    players, maxpoints = data

def test1():
    passed = []
    failed = {}
    
    for k,v in TEST_DATA.items():
        actual_value = part1(k)
        
        if actual_value == v:
            passed.append(k)
        else:
            failed[k] = (v, actual_value)
    
    return passed, failed

def part2(data=None, workers=None, base_duration=None, test=None):
    '''
    '''


class Field:
    def __init__(self, player_quantity, marble_quantity):
        self.player_scores = [0]*player_quantity
        self.marble_quantity = marble_quantity
        
        self.ring = Ring(0)
    
    def __iter__(self):
        pass
    
    def __next__(self):
        pass

class Ring(list):
    def __getitem__(self, key):
        if key < 0:
            key += len(self)
        
        return super().__getitem__(key)


if __name__=='__main__':
    from pprint import pformat
    import argparse
    import sys
    
    parser = argparse.ArgumentParser()
    parser.add_argument('part', type=int, help='which part to run')
    parser.add_argument('--test', action='store_true', help='run in test mode')
    
    args = parser.parse_args()
    
    if args.part == 1:
        if args.test:
            passed, failed = test1()
            
            print(f'passed: {pformat(passed)}')
            print(f'failed:\n{pformat(failed, indent=2)}')
        else:
            print(part1())
    elif args.part == 2:
        if args.test:
            passed, failed = test2()
            
            print(f'passed: {pformat(passed)}')
            print(f'failed:\n{pformat(failed, indent=2)}')
        else:
            print(part2())
    else:
        print(f'invalid part {args.part}', file=sys.stderr)
        sys.exit(1)
