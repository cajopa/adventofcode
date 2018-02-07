from collections import defaultdict


DEBUG = True


class Grid:
    INITAL_PATTERN = (False, True, False,
                      False, False, True,
                      True, True, True)
    
    
    def __init__(self, flat_values):
        flat_values = list(flat_values)
        
        self.size = int(len(flat_values) ** 0.5)
        self.values = defaultdict(bool, zip(((x,y) for y in range(self.size) for x in range(self.size)), flat_values))
    
    def __iter__(self):
        while True:
            self.blit()
            
            yield self
    
    def __eq__(self, other):
        flat_values = self.flat()
        
        return (
            flat_values == self.rotate_clockwise() or
            flat_values == rotate_counterclockwise() or
            flat_values == rotate_halfturn() or
            flat_values == reflect_vertical() or
            flat_values == reflect_horizontal()
        )
    
    @classmethod
    def from_text(cls, text):
        return cls(x == '#' for x in text if x != '/')
    
    @classmethod
    def combine(self, subgrids):
        pass
    
    ######### basic operations #########
    
    def flat(self):
        return [self.values[x,y] for y in range(self.size) for x in range(self.size)]
    
    def rotate_clockwise(self):
        return [self.values[x,y] for x in range(self.size) for y in reversed(range(self.size))]
    
    def rotate_counterclockwise(self):
        return [self.values[x,y] for x in reversed(range(self.size)) for y in range(self.size)]
    
    def rotate_halfturn(self):
        return [self.values[x,y] for y in reversed(range(self.size)) for x in reversed(range(self.size))]
    
    def reflect_vertical(self):
        return [self.values[x,y] for y in reversed(range(self.size)) for x in range(self.size)]
    
    def reflect_horizontal(self):
        return [self.values[x,y] for y in range(self.size) for x in reversed(range(self.size))]
    
    ######### 
    
    def blit(self):
        pass
    
    def enhance2(self):
        pass
    
    def enhance3(self):
        pass
    
    def split(self, target_size):
        pass
    
