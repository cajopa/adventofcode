DEBUG = False

def escape(instructions):
    steps = 0
    current = 0
    
    try:
        while True:
            if DEBUG:
                print '{}:'.format(current), ' '.join(('({})'.format(x) if i == current else str(x) for i,x in enumerate(instructions)))
            
            old_current = current
            offset = instructions[current]
            current += offset #if we've overflowed, this will raise an IndexError and we're done
            
            if offset < 3:
                instructions[old_current] += 1
            else:
                instructions[old_current] -= 1
            
            steps += 1
    except IndexError:
        return steps

def run(input_filename):
    instructions = []
    
    with open(input_filename, 'r') as f:
        for line in f:
            instructions.append(int(line.strip()))
    
    return escape(instructions)
