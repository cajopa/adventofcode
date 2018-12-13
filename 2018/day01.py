from itertools import count


def load(input_filename):
    with open(input_filename, 'r') as f:
        for line in f:
            yield int(line.strip())

def part1():
    input_data = load('input/1')
    
    return sum(input_data)

def part2():
    seen_frequencies = {0}
    current_frequency = 0
    
    for i in count(1):
        print('starting loop #{:d}'.format(i))
        
        frequency_changes = load('input/1')
        
        for datum in frequency_changes:
            current_frequency += datum
            
            if current_frequency in seen_frequencies:
                return current_frequency
            else:
                seen_frequencies.add(current_frequency)
