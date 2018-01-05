from collections import defaultdict
from itertools import count
from multiprocessing import Process, Pipe, Lock

DEBUG = True


class TandemProcessor(object):
    def __init__(self, instructions, pipe_to_other, pipe_home, receive_lock, program_id):
        super(TandemProcessor, self).__init__()
        
        self.instructions = instructions
        self.pipe_to_other = pipe_to_other
        self.pipe_home = pipe_home
        self.waiting = receive_lock
        
        self.reset()
        
        self.program_id = program_id
        self.registers['p'] = program_id
    
    def __getitem__(self, key):
        if key in self.registers:
            return self.registers[key]
        else:
            return int(key)
    
    def run(self):
        while True:
            try:
                instruction = self.instructions[self.program_counter]
                if DEBUG:
                    print '{}: {} @ {}'.format(self.program_id, instruction, self.program_counter)
                self.do(instruction)
            except Deadlocked:
                if DEBUG:
                    print '{}: received deadlock - terminating'.format(self.program_id)
                
                if self.pipe_home:
                    self.pipe_home.close()
                
                return
    
    def reset(self):
        self.program_counter = 0
        self.registers = defaultdict(lambda: 0)
    
    def do(self, bits):
        if getattr(self, '_{}'.format(bits[0]))(*bits[1:]) is None:
            self.program_counter += 1
    
    def _snd(self, register):
        if DEBUG:
            print '{}: sending {}'.format(self.program_id, self[register])
        
        self.pipe_to_other.send(self[register])
        
        if self.pipe_home:
            self.pipe_home.send(True)
    
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
        
        if self.waiting.acquire(block=False):
            if self.pipe_to_other.poll(5):
                self.registers[register] = self.pipe_to_other.recv()
                self.waiting.release()
            else:
                if DEBUG:
                    print '{}: DEADLOCKED'.format(self.program_id)
                
                if self.pipe_home:
                    self.pipe_home.close()
                raise Deadlocked
        else:
            if DEBUG:
                print '{}: DEADLOCKED'.format(self.program_id)
            
            if self.pipe_home:
                self.pipe_home.close()
            
            self.pipe_to_other.close()
            
            raise Deadlocked
    
    def _jgz(self, register, value):
        if self.registers[register] > 0:
            self.program_counter += self[value]
            return self.program_counter

class Deadlocked(Exception):
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
