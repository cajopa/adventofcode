from collections import defaultdict, Counter
import logging

logging.basicConfig(level=logging.DEBUG)


def load(input_filename):
    with open(input_filename, 'r') as f:
        return [x.strip().split(' ') for x in f]

def run1():
    cpu = Coprocessor(load('day23.input'))
    
    cpu.run()
    
    return cpu.stats

def run2():
    return algorithm_o2(a=1)


def algorithm_o1(a=0):
    b=c=d=e=f=g=h = 0
    
    def log_state():
        logging.debug(' '.join(map(str, (a,b,c,d,e,f,g,h))))
    
    log_state()
    
    if a == 0:
        b = c = 93
    else:
        b = 109300
        c = 126300
    
    log_state()

    for b in range(b, c+1, 17):
        f = 0
        log_state()
        
        for d in range(2, b+1):
            for e in range(b//d, b+1):
                if d*e == b:
                    f = 1
                    break
            if f:
                break
        
        if f:
            h += 1
        
        log_state()
    
    return h

def algorithm_o2(a=0):
    b=c=d=e=f=g=h = 0
    
    def log_state():
        logging.debug(' '.join(map(str, (a,b,c,d,e,f,g,h))))
    
    log_state()
    
    if a == 0:
        b = c = 93
    else:
        b = 109300
        c = 126300
    
    log_state()
    
    primes = eratosthenes_sieve(c)
    
    return len(set(range(b, c+1, 17)) - primes)

def eratosthenes_sieve(max_n):
    from math import ceil
    
    bad_n = set(range(4, max_n+1, 2))
    
    for n in range(3,int(ceil(max_n**0.5))+1,2):
        bad_n.update(range(2*n,max_n+1,n))
    
    return set(range(2,max_n+1)) - bad_n

def prime_factors(n, primes):
    return [p for p in primes if n%p == 0]


class Coprocessor:
    def __init__(self, instructions, initial_values={}):
        self.registers = defaultdict(int, initial_values)
        self.program_counter = 0
        self.program = instructions
        self.stats = Counter()
    
    @property
    def current_instruction(self):
        return self.program[self.program_counter]
    
    def do(self, instruction, *operands):
        logging.debug(' '.join((instruction,) + operands))
        
        if not getattr(self, instruction)(*operands):
            self.program_counter += 1
    
    def run(self):
        while self.program_counter < len(self.program):
            self.do(*self.current_instruction)
    
    def register_or_value(self, key):
        try:
            return int(key)
        except ValueError:
            return self.registers[key]
    
    def set(self, x, y):
        self.stats.update(['set'])
        
        self.registers[x] = self.register_or_value(y)
    
    def sub(self, x, y):
        self.stats.update(['sub'])
        
        self.registers[x] -= self.register_or_value(y)
    
    def mul(self, x, y):
        self.stats.update(['mul'])
        
        self.registers[x] *= self.register_or_value(y)
    
    def jnz(self, x, y):
        self.stats.update(['jnz'])
        
        if self.register_or_value(x) != 0:
            self.program_counter += self.register_or_value(y)
            
            return True
