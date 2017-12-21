from collections import defaultdict

DEBUG = True


class Processor(object):
    def __init__(self, instructions):
        self.instructions = instructions
        
        self.reset()
    
    def __getitem__(self, key):
        if key in self.registers:
            return self.registers[key]
        else:
            return int(key)
    
    def run(self):
        try:
            while True:
                self.do(self.instructions[self.program_counter])
        except ReceiveSignal as e:
            return e.frequency
    
    def reset(self):
        self.program_counter = 0
        self.registers = defaultdict(lambda: 0)
        self.last_sound = None
    
    def do(self, bits):
        if getattr(self, bits[0])(*bits[1:]) is None:
            self.program_counter += 1
    
    def snd(self, register):
        self.last_sound = self.registers[register]
    
    def set(self, register, value):
        self.registers[register] = self[value]
    
    def add(self, register, value):
        self.registers[register] += self[value]
    
    def mul(self, register, value):
        self.registers[register] *= self[value]
    
    def mod(self, register, other):
        self.registers[register] %= self[other]
    
    def rcv(self, register):
        if self.registers[register] != 0:
            raise ReceiveSignal(self.last_sound)
    
    def jgz(self, register, value):
        if self.registers[register] > 0:
            self.program_counter += self[value]
            return self.program_counter


class ReceiveSignal(Exception):
    def __init__(self, frequency):
        self.frequency = frequency


def load(input_filename='day18.input'):
    with open(input_filename, 'r') as f:
        return [line.strip().split(' ') for line in f if line.strip()]

def run1():
    return Processor(load()).run()
