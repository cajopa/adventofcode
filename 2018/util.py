from pprint import pformat
import argparse
import sys


def run_as_script(part1, test_data1, part2, test_data2):
    parser = argparse.ArgumentParser()
    parser.add_argument('part', type=int, help='which part to run')
    parser.add_argument('--test', action='store_true', help='run in test mode')

    args = parser.parse_args()

    if args.part == 1:
        function = part1
        test_data = test_data1
    elif args.part == 2:
        function = part2
        test_data = test_data2
    else:
        print(f'invalid part {args.part}', file=sys.stderr)
        sys.exit(-1)
    
    if args.test:
        passed, failed = test(function, test_data)
        
        if failed:
            print(f'passed: {pformat(passed)}')
            print(f'failed:\n{pformat(failed, indent=2)}')
        else:
            print('Everything is golden, my dude.')
        
        sys.exit(len(failed))
    else:
        print(function())

def test(function, test_data):
    passed = []
    failed = {}
    
    for k,v in test_data.items():
        actual_value = function(k)
        
        if actual_value == v:
            passed.append(k)
        else:
            failed[k] = (v, actual_value)
    
    return passed, failed
