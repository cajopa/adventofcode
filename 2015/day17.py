from collections import defaultdict


DEBUG = False

DEFAULT_INPUT = 'input/day17'
TOTAL_VOLUME = 150


def load(input_filename=DEFAULT_INPUT):
    with open(input_filename, 'r') as f:
        for line in f:
            yield int(line)

def run1():
    containers = tuple(load())
    
    return len(list(generate_combinations(containers)))

def run2():
    containers = tuple(load())
    
    container_counts = defaultdict(lambda: 0)
    
    for container_set in generate_combinations(containers):
        container_counts[len(container_set)] += 1
    
    return container_counts[min(container_counts.keys())]

def generate_combinations(containers, total=TOTAL_VOLUME):
    filtered_containers = tuple(sorted((x for x in containers if x <= total), reverse=True))
    
    for i, mycontainer in enumerate(filtered_containers):
        if mycontainer == total:
            if DEBUG:
                print('matched mycontainer ({})'.format(mycontainer))
            
            yield (total,)
        
        subcontainers = filtered_containers[i+1:]
        
        if len(subcontainers) == 1:
            maybe_yield = (mycontainer,) + subcontainers
            
            if DEBUG:
                print('need {}, got {}, tried {!r} - '.format(total, sum(maybe_yield), maybe_yield), end='')
            
            if sum(maybe_yield) == total:
                if DEBUG:
                    print('YIELD')
                
                yield maybe_yield
            elif DEBUG:
                print('IGNORE')
        else:
            for subcontainer_subset in generate_combinations(subcontainers, total=total-mycontainer):
                maybe_yield = (mycontainer,) + subcontainer_subset
                
                if DEBUG:
                    print('need {}, got {}, tried {!r} - '.format(total, sum(maybe_yield), maybe_yield), end='')
                
                if sum(maybe_yield) == total:
                    if DEBUG:
                        print('YIELD')
                    
                    yield maybe_yield
                elif DEBUG:
                    print('IGNORE')
