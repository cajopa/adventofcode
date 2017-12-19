DEBUG = False

class clist(list):
    def __init__(self, values):
        super(clist, self).__init__(values)
        self.current_index = 0
    
    def __getitem__(self, key):
        return super(clist, self).__getitem__(key % len(self))
    
    def __setitem__(self, key, value):
        return super(clist, self).__setitem__(key % len(self), value)
    
    def __delitem__(self, key):
        raise NotImplemented
    
    def __getslice__(self, start, end):
        new_start = start % len(self)
        new_end = end % len(self)
        
        if new_start < new_end:
            return super(clist, self).__getslice__(new_start, new_end)
        else:
            return super(clist, self).__getslice__(new_start, len(self)) + super(clist, self).__getslice__(0, new_end)
    
    def __setslice__(self, start, end, value):
        itervalue = iter(value)
        
        for i in range(start, end):
            self[i % len(self)] = next(itervalue)
    
    def __delslice__(self, start, end):
        raise NotImplemented


class KnotHashList(clist):
    def __init__(self, size):
        super(KnotHashList, self).__init__(range(size))
        
        self.skip_size = 0
    
    def pinch_and_twist(self, length):
        self[self.current_index:self.current_index+length] = reversed(self[self.current_index:self.current_index+length])
        self.current_index += length + self.skip_size
        self.skip_size += 1

def load(input_filename):
    with open(input_filename, 'r') as f:
        return map(int, f.read().strip().split(','))

def part1(lengths, size=256):
    knot = KnotHashList(size)
    
    if DEBUG:
        print '{0} cur {0.current_index} skip {0.skip_size}'.format(knot)
    
    for length in lengths:
        knot.pinch_and_twist(length)
        
        if DEBUG:
            print '{0} cur {0.current_index}/{1} skip {0.skip_size}'.format(knot, knot.current_index % len(knot))
    
    return knot[0] * knot[1]

def run1(input_filename='day10.input'):
    return part1(load(input_filename))
