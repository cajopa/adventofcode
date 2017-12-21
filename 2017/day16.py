import re


DEBUG = True


def load(input_filename='day16.input'):
    with open(input_filename, 'r') as f:
        for chunk in f.read().strip().split(','):
            if DEBUG:
                print 'loading {}'.format(chunk)
            
            yield parse_step(chunk)

def parse_step(text):
    match = re.match(r's(?P<amount>\d+)', text)
    if match:
        groupdict = match.groupdict()
        amount = int(groupdict['amount'])
        
        if DEBUG:
            print 'matched s: {}'.format(groupdict)
        
        return lambda word: spin(word, amount)
    
    match = re.match(r'x(?P<pos1>\d+)/(?P<pos2>\d+)', text)
    if match:
        groupdict = match.groupdict()
        pos1 = int(groupdict['pos1'])
        pos2 = int(groupdict['pos2'])
        
        if DEBUG:
            print 'matched x: {}'.format(groupdict)
        
        return lambda word: exchange(word, pos1, pos2)
    
    match = re.match(r'p(?P<name1>[a-z])/(?P<name2>[a-z])', text)
    if match:
        groupdict = match.groupdict()
        name1 = groupdict['name1']
        name2 = groupdict['name2']
        
        if DEBUG:
            print 'matched p: {}'.format(groupdict)
        
        return lambda word: partner(word, name1, name2)

def run1(size=16, steps=None):
    lineup = get_lineup(size)
    
    if steps is None:
        steps = load()
    
    for step in steps:
        lineup = step(lineup)
    
    return lineup

def run2(size=16, steps=None, rounds=10**9):
    lineup = get_lineup(size)
    
    if steps is None:
        steps = tuple(load())
    
    old_states = [lineup]
    
    for i in xrange(rounds):
        for step in steps:
            lineup = step(lineup)
        
        if lineup == old_states[0]:
            print 'found a duplicate! i={} len={}'.format(i, len(old_states))
            return old_states[rounds%len(old_states)]
        else:
            old_states.append(lineup)
    
    return lineup

def get_lineup(size):
    return ''.join([chr(ord('a') + i) for i in range(size)])

def spin(word, amount):
    return word[-amount:] + word[:-amount]

def exchange(word, position1, position2):
    if position1 > position2:
        position1, position2 = position2, position1 
    
    return word[:position1] + word[position2] + word[position1+1:position2] + word[position1] + word[position2+1:]

def partner(word, name1, name2):
    return exchange(word, word.find(name1), word.find(name2))
