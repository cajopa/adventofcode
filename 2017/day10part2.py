import operator as op

from day10 import KnotHashList


DEBUG = True

'''
input is string of bytes
append [17, 31, 73, 47, 23] to length sequence
run 64 rounds
  - same length sequence
  - preserve current_index and skip_size
split into blocks of 16, xor together
return hexadecimal
'''

def load(input_filename='day10.input'):
    with open(input_filename, 'rb') as f:
        return [ord(x) for x in f.read().strip()]

def run():
    return KnotHash(load()).hexdigest()


class KnotHash(object):
    def __init__(self, lengths, size=256):
        if isinstance(lengths, str):
            lengths = [ord(x) for x in lengths]
        
        self.lengths = list(lengths) + [17, 31, 73, 47, 23]
        self.knot = KnotHashList(size)
    
    def digest(self):
        for i in range(64):
            self.run_round()
        
        chunks = self.split()
        dense_chunks = [self.densify(x) for x in chunks]
        
        return ''.join((chr(x) for x in dense_chunks))
    
    def hexdigest(self):
        return ''.join((hex(ord(x))[2:] for x in self.digest()))
    
    def run_round(self):
        for length in self.lengths:
            self.knot.pinch_and_twist(length)
    
    def split(self):
        for i in range(0, len(self.knot), 16):
            yield self.knot[i:i+16]
    
    @staticmethod
    def densify(chunk):
        return reduce(op.xor, chunk, 0)
