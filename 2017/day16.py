import re


DEBUG = True


def load(input_filename='day16.input'):
    with open(input_filename, 'r') as f:
        for chunk in f.read().strip().split(','):
            if DEBUG:
                print 'loading {}'.format(chunk)
            
            match = re.match(r's(?P<amount>\d+)', chunk)
            if match:
                groupdict = match.groupdict()
                amount = int(groupdict['amount'])
                
                if DEBUG:
                    print 'matched s: {}'.format(groupdict)
                
                yield lambda word: spin(word, amount)
                continue
            
            match = re.match(r'x(?P<pos1>\d+)/(?P<pos2>\d+)', chunk)
            if match:
                groupdict = match.groupdict()
                pos1 = int(groupdict['pos1'])
                pos2 = int(groupdict['pos2'])
                
                if DEBUG:
                    print 'matched x: {}'.format(groupdict)
                
                yield lambda word: exchange(word, pos1, pos2)
                continue
            
            match = re.match(r'p(?P<name1>[a-z])/(?P<name2>[a-z])', chunk)
            if match:
                groupdict = match.groupdict()
                name1 = groupdict['name1']
                name2 = groupdict['name2']
                
                if DEBUG:
                    print 'matched p: {}'.format(groupdict)
                
                yield lambda word: partner(word, name1, name2)
                continue

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
    
    try:
        for i in xrange(rounds):
            if DEBUG and i%1000==0:
                print 'round {}'.format(i)
            
            for step in steps:
                lineup = step(lineup)
    except:
        if DEBUG:
            import pdb; pdb.post_mortem()
        else:
            raise
    
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
