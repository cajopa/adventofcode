DEBUG = False
input_value = 386


def run1(skip=input_value, steps=2017):
    final_state = generate(skip, steps)
    
    return final_state[(final_state.index(max(final_state)) + 1) % len(final_state)]

def run2(skip=input_value, steps=50000000):
    return find_last_oneth(skip, steps)

def generate(skip=input_value, steps=2017):
    state = [0]
    current_index = 0
    
    if DEBUG:
        print ' '.join(map(str, state))
    
    for i in xrange(steps):
        # insert_index = skip % len(state) + 1 - i
        current_index = (current_index + skip) % len(state) + 1
        
        if DEBUG:
            print 'i: {}, insert index: {}'.format(i, current_index)
        
        state.insert(current_index, i+1)
        
        if DEBUG:
            print ' '.join(map(str, state))
    
    return state

def find_last_oneth(skip=input_value, steps=50000000):
    current_index = 0
    to_return = None
    
    for i in xrange(steps):
        current_index = (current_index + skip) % (i+1) + 1
        
        if current_index == 1:
            to_return = i+1
    
    return to_return
