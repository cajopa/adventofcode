DEBUG = True

def load(input_filename):
    with open(input_filename, 'r') as f:
        return f.read().strip()

def run1(input_filename=None):
    return count_recipients(load(input_filename or 'input/day03'))

def run2(input_filename=None):
    return count_alternating_recipients(load(input_filename or 'input/day03'))

def find_recipients(instructions):
    visited = {(0,0)}
    current_x, current_y = (0,0)
    
    for instruction in instructions:
        if instruction == '<':
            current_x -= 1
        elif instruction == '>':
            current_x += 1
        elif instruction == '^':
            current_y += 1
        elif instruction == 'v':
            current_y -= 1
        
        visited.add((current_x, current_y))
    
    return visited

def count_recipients(instructions):
    return len(find_recipients(instructions))

def count_alternating_recipients(instructions):
    return len(find_recipients(instructions[0::2]) | find_recipients(instructions[1::2]))
