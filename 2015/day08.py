DEBUG = False

def load(input_filename='input/day08'):
    with open(input_filename, 'r') as f:
        for line in (x.strip() for x in f):
            yield line

def run1():
    return sum((len(line) - len(eval(line)) for line in load()))

def run2():
    
    return sum((len(reescape(line)) - len(line) for line in load()))

def reescape(value):
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
