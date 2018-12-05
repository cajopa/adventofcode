from collections import Counter


def load(input_filename):
    with open(input_filename, 'r') as f:
        return f.read().strip()

def part1(data=None, debug=False):
    data = data or load('input/5')
    
    current_polymer = data
    
    if debug:
        print(current_polymer)
    
    while True:
        # next_polymer = ''.join(_react(current_polymer))
        next_polymer = _minireact(current_polymer)
        
        if current_polymer == next_polymer:
            break
        else:
            current_polymer = next_polymer
            
            if debug:
                print(current_polymer)
    
    return current_polymer

def part2(data=None, debug=False):
    data = data or load('input/5')
    
    letter_histogram = Counter(data.lower())
    
    return min(((x,len(part1(data=data.replace(x,'').replace(x.upper(),'')))) for x in (y for y,_ in letter_histogram.most_common())), key=lambda x: x[1])

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

def _minireact(data):
    #find and destroy the first reacting pair, and return the rest (so dumb!)
    
    for i,(a,b) in enumerate(zip(data, data[1:].swapcase())):
        if a == b:
            return data[:i] + data[i+2:]
    
    return data
