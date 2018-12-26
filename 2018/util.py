from pprint import pformat
import argparse
import sys

import pytest


def run_as_script(day):
    parser = argparse.ArgumentParser()
    parser.add_argument('part', type=int, nargs='?', default=None, help='which part to run')
    parser.add_argument('--test', '-t', action='store_true', help='run in test mode')
    parser.add_argument('--debug', '-d', action='store_true', help='display debug messages')
    parser.add_argument('--pdb', action='store_true', help='launch pdb if test fails')

    args = parser.parse_args()

    if args.part:
        if args.part == 1:
            function = part1
        elif args.part == 2:
            function = part2
        else:
            print(f'invalid part {args.part}', file=sys.stderr)
            sys.exit(-1)
    
    if args.debug:
        function.__globals__['DEBUG'] = True
    
    if args.test:
        pytest_args = ['--pyargs', f'tests.day{day}']
        
        if args.pdb:
            pytest_args.append('--pdb')
        
        if args.part:
            pytest_args.extend(['-k', f'part{args.part} or Part{args.part}'])
        
        sys.exit(pytest.main(pytest_args))
    else:
        print(function())
