from pprint import pformat
import argparse
import sys


def run_as_script(part1, test_data1, part2, test_data2):
    parser = argparse.ArgumentParser()
    parser.add_argument('part', type=int, help='which part to run')
    parser.add_argument('--test', action='store_true', help='run in test mode')

    args = parser.parse_args()

    if args.part == 1:
        if args.test:
            passed, failed = test(part1, test_data1)
            
            print(f'passed: {pformat(passed)}')
            print(f'failed:\n{pformat(failed, indent=2)}')
        else:
            print(part1())
    elif args.part == 2:
        if args.test:
            passed, failed = test(part2, test_data2)
            
            print(f'passed: {pformat(passed)}')
            print(f'failed:\n{pformat(failed, indent=2)}')
        else:
            print(part2())
    else:
        print(f'invalid part {args.part}', file=sys.stderr)
        sys.exit(1)

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
