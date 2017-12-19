def load(input_filename):
    with open(input_filename, 'r') as f:
        return [int(x.strip()) for x in f.read().split('\t') if x]

def reallocate(banks):
    #find first bank with maximum
    max_alloc = max(banks)
    realloc_index, realloc_value = [(i,x) for i,x in enumerate(banks) if x==max_alloc][0]
    
    #set it to zero
    banks[realloc_index] = 0
    
    #distribute evenly
    ## use divmod to reduce the need for more looping - doesn't quite work
    # whole_trips, partial_trip_length = divmod(realloc_value, len(banks))
    # return [x + whole_trips + (1 if partial_trip_length and (i - realloc_index + 1) % len(banks) <= partial_trip_length else 0) for i,x in enumerate(banks)]
    
    to_return = banks[:]
    
    for i in range(realloc_value):
        to_return[(realloc_index + i + 1) % len(banks)] += 1
    
    return to_return

def run(find_collision):
    return find_collision(load('day06.input'))
