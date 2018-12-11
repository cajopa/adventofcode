from functools import reduce
import operator as op
import re


def load(input_filename):
    with open(input_filename, 'r') as f:
        pattern = re.compile(r'Step (?P<predicate>.) must be finished before step (?P<consequent>.) can begin.')
        
        for line in f:
            match = pattern.match(line.strip())
            
            yield match.group('predicate'), match.group('consequent')

def common_part(data=None, test=False, workers=None, base_duration=None):
    raw_instructions = list(data or (test and load('input/7.test')) or load('input/7'))
    workers = workers or (test and 2) or 5
    base_duration = base_duration or (test and 0) or (not test and 60)
    
    steps = {}
    
    #first pass creates the steps bare
    for pre, con in raw_instructions:
        steps.setdefault(con, Step(con, base_duration=base_duration))
        steps.setdefault(pre, Step(pre, base_duration=base_duration))
    
    #second pass hooks them up
    for pre, con in raw_instructions:
        steps[pre].consequents.add(steps[con])
        steps[con].predicates.add(steps[pre])
    
    return Instructions(steps.values(), workers=workers)

def part1(data=None, test=False):
    '''
    In what order should the steps in your instructions be completed?
    
    If more than one step is ready, choose the step which is first alphabetically.
    '''
    
    return iter(common_part(data, test))

def part2(data=None, workers=None, base_duration=None, test=False):
    '''
    With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
    
    Each step takes 60 seconds plus an amount corresponding to its letter.
    '''
    
    return common_part(data=data, test=test, workers=workers, base_duration=base_duration)


class Step:
    def __init__(self, name, predicates=[], consequents=[], base_duration=0):
        self.name = name
        self.predicates = set(predicates)
        self.consequents = set(consequents)
        self.base_duration = name and base_duration + ord(name) - ord('A') + 1
        
        self.instructions = None
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'
    __str__=__repr__

class Instructions:
    def __init__(self, steps, workers=1):
        self.steps = set()
        
        self._current = None
        self.completed = None
        self.workers = workers
        
        for step in steps:
            step.instructions = self
            self.steps.add(step)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} @{self.current}>'
    __str__=__repr__
    
    def __iter__(self):
        self.completed = set()
        self.current = self.preroot
        
        return self
    
    def __next__(self):
        'The step that should be executed next.'
        
        ready = self.ready
        
        if len(ready) == 0:
            raise StopIteration
        elif len(ready) == 1:
            self.current = ready.pop()
        else:
            self.current = sorted(ready, key=lambda x: x.name)[0]
        
        return self.current
    
    def __getitem__(self, key):
        try:
            return next(x for x in self.steps if x.name == key)
        except:
            raise KeyError(key)
    
    @property
    def current(self):
        return self._current
    
    @current.setter
    def current(self, value):
        self.completed.add(value)
        self._current = value
    
    @property
    def roots(self):
        'Find nodes with no parents.'
        
        candidates = {x for x in self.steps if not x.predicates}
        
        if len(candidates) == 0:
            raise Exception('Root not found!')
        else:
            return candidates
    
    @property
    def preroot(self):
        'A virtual node that acts as a starting point for walking.'
        
        return Step(None, consequents=self.roots)
    
    @property
    def ready(self):
        '''
        The steps that are ready to be executed.
        All predicates must be satisfied for a node to be ready.
        '''
        
        candidates = reduce(op.or_, (x.consequents for x in self.completed))
        satisfied = {x for x in candidates if x.predicates <= self.completed}
        
        return satisfied - self.completed
