def load(input_filename):
    with open(input_filename, 'r') as f:
        return f.read().strip()

def part1(data=None):
    data = data or load('input/5')
    
    current_polymer = data
    
    while True:
        next_polymer = ''.join(_react(current_polymer))
        
        if current_polymer == next_polymer:
            break
        else:
            current_polymer = next_polymer
    
    return current_polymer

def part2():
    pass

def _react(data):
    previous = []
    
    for current in data:
        if len(previous) == 2:
            if previous[0] != previous[1].swapcase():
                yield from previous
            
            previous = [current]
        elif len(previous) == 1:
            if current == previous[0].swapcase():
                previous.append(current)
            else:
                yield previous[0]
                previous = [current]
        else:
            previous.append(current)
    
    if previous:
        yield from previous
