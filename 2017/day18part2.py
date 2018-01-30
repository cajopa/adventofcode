from collections import defaultdict
from itertools import count

DEBUG = True


def load(input_filename='day18.input'):
    with open(input_filename, 'r') as f:
        return [line.strip().split(' ') for line in f if line.strip()]

def run(instructions=None):
    if not instructions:
        instructions = load()
    
    manager = ProcessorManager(instructions)
    manager.run()
    
    processor1_state = manager.current if manager.current.processor.program_id == 1 else manager.other
    return processor1_state.processor.send_count


class ProcessorManager:
    def __init__(self, instructions):
        self.current = ProcessorState(TandemProcessor(instructions, 0))
        self.other = ProcessorState(TandemProcessor(instructions, 1))
    
    def run(self):
        for i in count(1):
            self.current.last_value = next(self.current.iterator)
            
            if self.current.last_value is TandemProcessor.WAITING:
                if self.other.last_value is TandemProcessor.WAITING:
                    return i
                else:
                    self.switch()
            else:
                self.other.processor.queue(self.current.last_value)
    
    def switch(self):
        self.current, self.other = self.other, self.current

class ProcessorState:
    def __init__(self, processor):
        self.processor = processor
        self.iterator = iter(processor)
        self.last_value = None

class TandemProcessor:
    WAITING = object()
    
    
    def __init__(self, instructions, program_id):
        super(TandemProcessor, self).__init__()
        
        self.instructions = instructions
        
        self.program_counter = 0
        self.registers = defaultdict(lambda: 0)
        self.receive_queue = []
        self.send_count = 0
        
        self.program_id = program_id
        self.registers['p'] = program_id
    
    def __iter__(self):
        while True:
            command, *args = self.instructions[self.program_counter]
            
            if DEBUG:
                print('{}: {}({}) @ {}'.format(self.program_id, command, ', '.join(args), self.program_counter))
            
            if command == 'snd':
                yield from self._snd(*args)
            elif command == 'rcv':
                yield from self._rcv(*args)
            else:
                self.do(command, *args)
    
    def register(self, key):
        if key in self.registers:
            return self.registers[key]
        else:
            return int(key)
    
    def do(self, command, *args):
        if getattr(self, '_{}'.format(command))(*args) is None:
            self.program_counter += 1
    
    def queue(self, value):
        self.receive_queue.append(value)
    
    def _snd(self, register):
        if DEBUG:
            print('{}: sending {}'.format(self.program_id, self.register(register)))
        
        self.send_count += 1
        
        yield self.register(register)
        
        self.program_counter += 1
    
    def _set(self, register, value):
        self.registers[register] = self.register(value)
    
    def _add(self, register, value):
        self.registers[register] += self.register(value)
    
    def _mul(self, register, value):
        self.registers[register] *= self.register(value)
    
    def _mod(self, register, other):
        self.registers[register] %= self.register(other)
    
    def _rcv(self, register):
        while True:
            try:
                value = self.receive_queue.pop(0)
            except IndexError:
                yield self.WAITING
            else:
                break
        
        if DEBUG:
            print('{}: receiving {} into {}'.format(self.program_id, value, register))
        
        self.registers[register] = value
        
        self.program_counter += 1
    
    def _jgz(self, register, value):
        if self.registers[register] > 0:
            self.program_counter += self.register(value)
            return self.program_counter
