from itertools import product
from collections import defaultdict
import math


DEBUG = True


class Matrix:
    def __init__(self, width, height, values):
        self.width = width
        self.height = height
        self.values = defaultdict(int)
        
        for p,v in zip(((x,y) for y in range(height) for x in range(width)), values):
            self.values[p] = v
    
    def __str__(self):
        max_digits = math.ceil(math.log10(max(self.values.values()) + 1))
        
        return '\n'.join(' '.join('{N: {L}d}'.format(N=self.values[x,y], L=max_digits) for x in range(self.width)) for y in range(self.height))
    
    def __mul__(self, other):
        if self.width == other.height:
            def inner():
                for x,y in ((x,y) for y in range(self.height) for x in range(other.width)):
                    yield self.row(y).dot_product(other.column(x))
            
            return self.__class__(other.width, self.height, inner())
        else:
            raise ValueError('Can only be multiplied by a matrix with {} rows'.format(self.width))
    
    def dot_product(self, other):
        if self.width == 1 and other.width == 1:
            return sum(x*y for x,y in zip(self.flat, other.flat))
        else:
            raise ValueError('Dot product only applies to vectors')
    
    def column(self, index):
        return self.__class__(1, self.height, (self.values[index, i] for i in range(self.height)))
    
    def row(self, index):
        return self.__class__(1, self.width, (self.values[i, index] for i in range(self.width)))
    
    @property
    def flat(self):
        return (self.values[x,y] for y in range(self.height) for x in range(self.width))


class Grid:
    INITAL_PATTERN = ((False, True, False),
                      (False, False, True),
                      (True, True, True))
    
    
    def __init__(self):
        pass
    
    def __iter__(self):
        while True:
            self.blit()
            
            yield self
    
    @classmethod
    def combine(self, subgrids):
        pass
    
    ######### basic operations #########
    
    
    
    ######### 
    
    def blit(self):
        pass
    
    def enhance2(self):
        pass
    
    def enhance3(self):
        pass
    
    def split(self, target_size):
        pass
    
