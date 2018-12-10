import re


def load(input_filename):
    with open(input_filename, 'r') as f:
        pattern = re.compile(r'Step (?P<predicate>.) must be finished before step (?P<consequent>.) can begin.')
        
        for line in f:
            match = pattern.match(line.strip())
            
            yield match.group('predicate'), match.group('consequent')

def common_part(data=None, test=False):
    raw_instructions = list(data or (test and load('input/7.test')) or load('input/7'))
    
    steps = {}
    
    #first pass creates the steps bare
    for pre, con in raw_instructions:
        steps.setdefault(con, Step(con))
        steps.setdefault(pre, Step(pre))
    
    #second pass hooks them up
    for pre, con in raw_instructions:
        steps[pre].consequents.add(steps[con])
        steps[con].consequents.add(steps[pre])
    
    return Instructions(steps.values())

def part1(data=None, test=False):
    '''
    In what order should the steps in your instructions be completed?
    
    If more than one step is ready, choose the step which is first alphabetically.
    '''
    
    return common_part(data, test).walk()

def part2(data=None, test=False):
    pass


class Step:
    def __init__(self, name, predicates=[], consequents=[]):
        self.name = name
        self.predicates = set(predicates)
        self.consequents = set(consequents)
        
        self.instructions = None
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'
    __str__=__repr__

class Instructions:
    def __init__(self, steps):
        self.steps = set()
        
        self.current = None
        
        for step in steps:
            step.instructions = self
            self.steps.add(step)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} @{self.current}>'
    __str__=__repr__
    
    @property
    def root(self):
        'Assumes only one root.'
        pass
    
    @property
    def ready(self):
        'The steps that are ready to be executed.'
        pass
    
    @property
    def next(self):
        'The step that should be executed next.'
        pass
    
    def walk(self):
        'Start at the root and yield steps in order.'
        pass
