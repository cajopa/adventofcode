DEBUG = True

def load(input_filename):
    with open(input_filename, 'r') as f:
        return f.read().strip()

def run1(input_filename=None):
    return find_floor(load(input_filename or 'input/day01'))

def run2(input_filename=None):
    return find_first_basement(load(input_filename or 'input/day01'))

def find_floor(instructions):
    current_floor = 0
    
    for instruction in instructions:
        if instruction == '(':
            current_floor += 1
        elif instruction == ')':
            current_floor -= 1
    
    return current_floor

def find_first_basement(instructions):
    current_floor = 0
    
    for i, instruction in enumerate(instructions):
        if instruction == '(':
            current_floor += 1
        elif instruction == ')':
            current_floor -= 1
        
        if current_floor < 0:
            return i+1
