import re


DEBUG = False

'''
group: starts with { and ends with }, can be nested

skip characters:
    - garbage: starts with <, ends with >, no nesting
    - bangskip: starts with !, consumes the following one character

part 1:
    goal: find total score
    definitions:
        score: sum of score of all groups
        score of group: parent.score + 1, root=1
    approach:
        - remove canceled characters
        - remove garbage
        - remove commas (not syntactically significant)
        - all that's left is braces, so track the level and tally the score iteratively
part 2:
    goal: count garbage characters, not including canceled or angle braces
    approach:
        - remove canceled characters
        - find all non-overlapping garbage via regex
'''

def load(input_filename):
    with open(input_filename, 'r') as f:
        return f.read().strip()

def part1(stream):
    return count_score(strip_commas(strip_garbage(strip_bangskips(stream))))

def part2(stream):
    return sum(map(len, get_all_garbage(strip_bangskips(stream))))

def run1(input_filename=None):
    return part1(load(input_filename or 'day09.input'))

def run2(input_filename=None):
    return part2(load(input_filename or 'day09.input'))

def strip_bangskips(stream):
    return re.sub(r'!.', '', stream)

def strip_garbage(stream):
    return re.sub(r'<.*?>', '', stream)

def strip_commas(stream):
    return stream.replace(',', '')

def count_score(stream):
    level = 0
    score = 0
    
    for character in stream:
        if character == '{':
            level += 1
            score += level
        else: # character == '}'
            level -= 1
    
    return score

def get_all_garbage(stream):
    matches = re.findall(r'<.*?>', stream)
    
    return [x[1:-1] for x in matches]
