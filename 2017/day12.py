import re


DEBUG = False


def load(input_filename='day12.input'):
    def inner():
        with open(input_filename, 'r') as f:
            for line in f:
                match = re.match(r'(?P<from_id>\d+) <-> (?P<to_ids>\d+(?:, \d+)*)', line.strip())
                
                groupdict = match.groupdict()
                from_id = int(groupdict['from_id'])
                to_ids = set(map(int, groupdict['to_ids'].split(', ')))
                
                yield from_id, to_ids
    
    return dict(inner())

def run1():
    return count_connected_to_zero(load())

def run2():
    return count_groups(load())

def count_connected_to_zero(connections):
    connections[0].add(0)
    
    return len(find_all_connected({0}, set(), connections))

def find_all_connected(parents, visited, connections):
    children = set()
    
    parents_to_check = parents - visited
    
    for parent in parents_to_check:
        children |= connections[parent]
        visited.add(parent)
    
    if children == parents:
        return children
    else:
        return children | find_all_connected(children, visited, connections)

def count_groups(connections):
    return len(set((frozenset(find_all_connected({i}, set(), connections)) for i in connections)))
