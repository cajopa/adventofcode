from collections import defaultdict
from itertools import count
from multiprocessing import Process, Pipe, Lock

DEBUG = True


class TandemProcessor(object):
    def __init__(self, instructions, program_id):
        super(TandemProcessor, self).__init__()
        
        self.instructions = instructions
        
        self.program_counter = 0
        self.registers = defaultdict(lambda: 0)
        
        self.program_id = program_id
        self.registers['p'] = program_id
    
    def __getitem__(self, key):
        if key in self.registers:
            return self.registers[key]
        else:
            return int(key)
    
    def run(self):
        while True:
            instruction = self.instructions[self.program_counter]
            
            if DEBUG:
                print '{}: {} @ {}'.format(self.program_id, instruction, self.program_counter)
            
            if instruction[0] == 'snd':
                pass
            elif instruction[0] == 'rcv':
                
            else:
                self.do(instruction)
    
    ##### ABANDON MULTIPROCESSING!! RUN ONE ITERATOR UNTIL IT YIELDS, THEN RUN THE OTHER
    
    @property
    def receiver(self):
        def inner():
            while True:
                register, value = (yield)
                self.registers[register] = value
        
        return next(inner())
    
    @property
    def transmitter(self):
        def inner():
            while True:
                
    
    def do(self, bits):
        if getattr(self, '_{}'.format(bits[0]))(*bits[1:]) is None:
            self.program_counter += 1
    
    def _snd(self, register):
        if DEBUG:
            print '{}: sending {}'.format(self.program_id, self[register])
        
        yield self[register]
    
    def _set(self, register, value):
        self.registers[register] = self[value]
    
    def _add(self, register, value):
        self.registers[register] += self[value]
    
    def _mul(self, register, value):
        self.registers[register] *= self[value]
    
    def _mod(self, register, other):
        self.registers[register] %= self[other]
    
    def _rcv(self, register):
        if DEBUG:
            print '{}: receiving into {}'.format(self.program_id, register)
        
        #TODO: deadlock detection
        
        self.registers[register] = (yield)
    
    def _jgz(self, register, value):
        if self.registers[register] > 0:
            self.program_counter += self[value]
            return self.program_counter

class Deadlocked(Exception):
    pass

class Waiting(Exception):
    pass


def load(input_filename='day18.input'):
    with open(input_filename, 'r') as f:
        return [line.strip().split(' ') for line in f if line.strip()]

def run(instructions=None):
    if not instructions:
        instructions = load()
    interconn1, interconn2 = Pipe()
    callhome0, callhome1 = Pipe(False)
    lock = Lock()
    
    Process(target=target, args=(instructions, interconn1, None, lock, 0)).start()
    Process(target=target, args=(instructions, interconn2, callhome1, lock, 1)).start()
    
    for i in count(1):
        try:
            if DEBUG:
                print 'home: {}'.format(i)
            
            if callhome0.poll(1):
                callhome0.recv()
            else:
                return i
        except EOFError:
            return i

def target(instructions, interpipe, homepipe, receive_lock, program_id):
    return TandemProcessor(instructions, interpipe, homepipe, receive_lock, program_id).run()
