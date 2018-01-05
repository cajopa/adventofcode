import re

from kids.cache import cache


DEBUG = False


def load(input_filename='input/day07'):
    with open(input_filename, 'r') as f:
        for line in (x.strip() for x in f):
            match = re.match(r'(?:(?P<arg01>[a-z0-9]+)|(?P<func1>NOT) (?P<arg11>[a-z0-9]+)|(?P<arg21>[a-z0-9]+) (?P<func2>[LR]SHIFT|OR|AND) (?P<arg22>[a-z0-9]+)) -> (?P<dest>[a-z]+)', line)
            
            if match.group('func2'):
                yield match.group('dest'), match.group('func2'), (match.group('arg21'), match.group('arg22'))
            elif match.group('func1'):
                yield match.group('dest'), match.group('func1'), (match.group('arg11'),)
            else:
                yield match.group('dest'), None, (match.group('arg01'),)

def run1():
    return Wireball(load())['a']

def run2():
    return Wireball(((('b', None, (run1(),)) if x[0] == 'b' else x) for x in load()))['a']


class Wireball(object):
    def __init__(self, wires):
        self.wires = {}
        
        for dest, func, args in wires:
            if func == 'NOT':
                wirefunc = self._not(*args)
            elif func == 'OR':
                wirefunc = self._or(*args)
            elif func == 'AND':
                wirefunc = self._and(*args)
            elif func == 'LSHIFT':
                wirefunc = self._lshift(*args)
            elif func == 'RSHIFT':
                wirefunc = self._rshift(*args)
            else: #SET
                wirefunc = self._set(*args)
            
            self[dest] = wirefunc
    
    def __getitem__(self, key):
        return self.wires.get(key, lambda: int(key))()
    
    def __setitem__(self, key, value):
        self.wires[key] = value
    
    def _set(self, value):
        @cache
        def inner():
            return self[value]
        
        return inner
    
    def _not(self, source):
        @cache
        def inner():
            return ~self[source] & 0xffff
        
        return inner
    
    def _or(self, source1, source2):
        @cache
        def inner():
            return self[source1] | self[source2]
        
        return inner
    
    def _and(self, source1, source2):
        @cache
        def inner():
            return self[source1] & self[source2]
        
        return inner
    
    def _lshift(self, source, value):
        @cache
        def inner():
            return self[source] << self[value] & 0xffff
        
        return inner
    
    def _rshift(self, source, value):
        @cache
        def inner():
            return self[source] >> self[value] & 0xffff
        
        return inner
