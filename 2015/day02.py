DEBUG = False

def load(input_filename):
    with open(input_filename, 'r') as f:
        for line in f:
            yield map(int, line.strip().split('x'))

def run1(input_filename=None):
    return find_paper(load(input_filename or 'input/day02'))

def run2(input_filename=None):
    return find_ribbon(load(input_filename or 'input/day02'))

class Box(object):
    def __init__(self, width, height, length):
        self.width = width
        self.height = height
        self.length = length
    
    @property
    def surface_area(self):
        return 2 * (self.width*self.height + self.width*self.length + self.height*self.length)
    
    @property
    def slack_paper(self):
        return reduce(lambda x,y: x*y, self.min2, 1)
    
    @property
    def wrapping_needed(self):
        return self.surface_area + self.slack_paper
    
    @property
    def min2(self):
        return list(sorted((self.width, self.height, self.length)))[:2]
    
    @property
    def smallest_perimeter(self):
        return 2*sum(self.min2)
    
    @property
    def volume(self):
        return self.width * self.height * self.length
    
    @property
    def ribbon_needed(self):
        return self.smallest_perimeter + self.volume

def find_paper(sizes):
    return sum((Box(w,h,l).wrapping_needed for w,h,l in sizes))

def find_ribbon(sizes):
    return sum((Box(w,h,l).ribbon_needed for w,h,l in sizes))
