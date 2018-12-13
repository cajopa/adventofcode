from functools import reduce
import operator as op
import re


def load(input_filename):
    with open(input_filename, 'r') as f:
        pattern = re.compile(r'Step (?P<predicate>.) must be finished before step (?P<consequent>.) can begin.')
        
        for line in f:
            match = pattern.match(line.strip())
            
            yield match.group('predicate'), match.group('consequent')

def common_part(data=None, test=False, step_class=None, **kwargs):
    raw_instructions = list(data or (test and load('input/7.test')) or load('input/7'))
    
    if 'base_duration' in kwargs and kwargs['base_duration'] is None:
        kwargs['base_duration'] = 0 if test else 60
    
    step_class = step_class or Step
    
    steps = {}
    
    #first pass creates the steps bare
    for pre, con in raw_instructions:
        steps.setdefault(con, step_class(con, **kwargs))
        steps.setdefault(pre, step_class(pre, **kwargs))
    
    #second pass hooks them up
    for pre, con in raw_instructions:
        steps[pre].consequents.add(steps[con])
        steps[con].predicates.add(steps[pre])
    
    return steps.values()

def part1(data=None, test=False):
    '''
    In what order should the steps in your instructions be completed?
    
    If more than one step is ready, choose the step which is first alphabetically.
    '''
    
    return SingleInstructions(common_part(data, test))

def part2(data=None, workers=None, base_duration=None, test=False):
    '''
    With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
    
    Each step takes 60 seconds plus an amount corresponding to its letter.
    '''
    
    return sum(x for _,x in _part2(data=data,workers=workers,base_duration=base_duration,test=test))

def _part2(data=None, workers=None, base_duration=None, test=False):
    return MultiInstructions(
        common_part(
            data=data,
            test=test,
            step_class=DurationStep,
            base_duration=base_duration
        ),
        workers=workers or (test and 2) or 5
    )


class Step:
    def __init__(self, name, predicates=[], consequents=[]):
        self.name = name
        self.predicates = set(predicates)
        self.consequents = set(consequents)
        
        self.instructions = None
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'
    
    def __str__(self):
        return self.__repr__()

class DurationStep(Step):
    def __init__(self, name, predicates=[], consequents=[], base_duration=0):
        super().__init__(name, predicates, consequents)
        
        self.duration = (base_duration + ord(name) - ord('A') + 1) if name else 0
        self.remaining_duration = self.duration

class BaseInstructions:
    def __init__(self, steps):
        self.steps = set()
        
        self.completed = None
        
        for step in steps:
            step.instructions = self
            self.steps.add(step)
    
    def __repr__(self):
        raise NotImplementedError
    
    def __str__(self):
        return self.__repr__()
    
    def __iter__(self):
        self.completed = {self.preroot}
        
        return self
    
    def __next__(self):
        'The step that should be executed next.'
        
        raise NotImplementedError
    
    def __getitem__(self, key):
        try:
            return next(x for x in self.steps if x.name == key)
        except:
            raise KeyError(key)
    
    @property
    def next_step(self):
        return self.next_steps[0]
    
    @property
    def next_steps(self):
        ready = self.ready
        
        if len(ready) == 0:
            raise StopIteration
        elif len(ready) == 1:
            return list(ready)
        else:
            return sorted(ready, key=lambda x: x.name)
    
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
        
        roots = self.roots
        
        to_return = Step(None, consequents=self.roots)
        
        for root in roots:
            root.predicates = {to_return}
        
        return to_return
    
    @property
    def ready(self):
        '''
        The steps that are ready to be executed.
        All predicates must be satisfied for a node to be ready.
        '''
        
        candidates = reduce(op.or_, (x.consequents for x in self.completed))
        satisfied = {x for x in candidates if x.predicates <= self.completed}
        
        return satisfied - self.completed

class SingleInstructions(BaseInstructions):
    def __repr__(self):
        return '<{self.__class__.__name__} completed {0}>'.format(
            'none' if self.completed is None else len(self.completed),
            self=self
        )
    
    def __next__(self):
        'The step that should be executed next.'
        
        current = self.next_step
        
        self.completed.add(current)
        
        return current

class MultiInstructions(BaseInstructions):
    def __init__(self, steps, workers=1):
        super().__init__(steps)
        
        self.workers = workers
        self.working = None
    
    def __repr__(self):
        return '<{self.__class__.__name__} completed {0}, working on {1}>'.format(
            'none' if self.completed is None else len(self.completed),
            'none' if self.working is None else len(self.working),
            self=self
        )
    
    def __iter__(self):
        self.working = set()
        
        return super().__iter__()
    
    def __next__(self):
        'The steps that just finished and the time elapsed since last time.'
        
        self.start_next()
        
        maybe_result = self.complete_shortest_working()
        
        if maybe_result:
            return maybe_result
        else:
            #if no steps completed, we're done
            raise StopIteration
    
    def start_next(self):
        if self.ready:
            #start next step(s)
            number_of_available_workers = self.workers - len(self.working)
            
            if number_of_available_workers:
                next_steps = self.next_steps
                
                self.working |= set(next_steps[:number_of_available_workers])
    
    def complete_shortest_working(self):
        if self.working:
            #complete the shortest working step(s), yield, and progress other working steps
            min_remaining_duration = min(x.remaining_duration for x in self.working)
            steps_to_complete = {x for x in self.working if x.remaining_duration == min_remaining_duration}
            
            self.working -= steps_to_complete
            self.completed |= steps_to_complete
            
            for step in self.working:
                step.remaining_duration -= min_remaining_duration
            
            return steps_to_complete, min_remaining_duration
    
    @property
    def ready(self):
        return super().ready - self.working
