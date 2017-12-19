import operator as op
import re


DEBUG = False


def load(input_filename):
    with open(input_filename, 'r') as f:
        for line in f:
            match = re.match(r'(?P<register>.+?) (?P<instruction>.+?) (?P<amount>.+?) if (?P<condition_target>.+?) (?P<operator>.+?) (?P<condition_value>.+)', line)
            
            groupdict = match.groupdict()
            register = groupdict['register']
            jump_amount = (-1 if groupdict['instruction'] == 'dec' else 1) * int(groupdict['amount'])
            
            if groupdict['operator'] == '==':
                operator = op.eq
            elif groupdict['operator'] == '!=':
                operator = op.ne
            elif groupdict['operator'] == '<':
                operator = op.lt
            elif groupdict['operator'] == '>':
                operator = op.gt
            elif groupdict['operator'] == '<=':
                operator = op.le
            elif groupdict['operator'] == '>=':
                operator = op.ge
            else:
                raise ValueError('invalid operator')
            
            condition = (groupdict['condition_target'], operator, int(groupdict['condition_value']))
            
            yield register, jump_amount, condition

def find_largest(instructions):
    registry = {}
    
    for register, jump_amount, condition in instructions:
        if DEBUG:
            print register, jump_amount, condition
        
        target, operator, value = condition
        
        if operator(registry.get(target, 0), value):
            if DEBUG: print 'condition passed'
            
            registry[register] = registry.get(register, 0) + jump_amount
            
            if DEBUG: print format_registry(registry)
    
    return max(registry.itervalues())

def find_largest_ever(instructions):
    def inner():
        registry = {}
        
        for register, jump_amount, condition in instructions:
            if DEBUG:
                print register, jump_amount, condition
            
            target, operator, value = condition
            
            if operator(registry.get(target, 0), value):
                if DEBUG: print 'condition passed'
                
                registry[register] = registry.get(register, 0) + jump_amount
                yield max(registry.itervalues())
                
                if DEBUG: print format_registry(registry)
    
    return max(inner())

def format_registry(registry):
    return ' '.join(['{}:{}'.format(k,v) for k,v in registry.iteritems()])

def run1(input_filename=None):
    return find_largest(load(input_filename or 'day08.input'))

def run2(input_filename=None):
    return find_largest_ever(load(input_filename or 'day08.input'))
