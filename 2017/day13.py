import itertools
import re


DEBUG = True


def load(input_filename='day13.input'):
    def inner():
        with open(input_filename, 'r') as f:
            for line in f:
                yield map(int, re.match(r'(\d+): (\d+)', line.strip()).groups())
    
    return dict(inner())

def run1():
    return Firewall(load()).severity

def run2():
    firewall = Firewall(load())
    
    for delay in itertools.count():
        if DEBUG:
            if delay > 10:
                print 'passed delay 10 - quitting'
                return
            
            any_collided = firewall.delay(delay).any_collides()
            
            print 'delay {:03d}, collided {}'.format(delay, 'yes' if any_collided else 'no')
            
            if not any_collided:
                return delay
        else:
            if not firewall.delay(delay).any_collides():
                return delay

def run2_smart(layerdata=None):
    minfw = layerdata or load()
    
    def scanner_position(delay, layer, size):
        ml = (delay + layer) % (2 * (size - 1))
        
        return ml if ml < size else 2*size - ml - 2
    
    def collides(delay, layer, size):
        spos = scanner_position(delay, layer, size)
        
        if DEBUG:
            return spos == 0, spos
        else:
            return spos == 0
    
    for delay in itertools.count():
        if DEBUG:
            collided = False
            
            for layer, size in minfw.iteritems():
                current_collides, spos = collides(delay, layer, size)
                if current_collides:
                    print 'delay {} layer {} (eff size {}) collides at {}'.format(delay, layer, 2*(size-1), spos)
                    collided = True
                    break
                else:
                    print 'delay {} layer {} (eff size {}) no collide: scanner {}'.format(delay, layer, 2*(size-1), spos)
            
            if not collided:
                return delay
        else:
            if not any((collides(delay, layer, size) for layer, size in minfw.iteritems())):
                return delay


class Firewall(object):
    def __init__(self, layers):
        self.layers = [Layer(layers.get(i, 0)) for i in range(max(layers)+1)]
        self.packet_position = -1
    
    def __str__(self):
        return '\n'.join('{}: {}'.format(i, l) for i,l in enumerate(self.layers))
    
    def increment(self):
        self.packet_position += 1
        
        if DEBUG:
            print 'incrementing to {}'.format(self.packet_position)
        
        collided = self.collides
        
        if DEBUG:
            print 'collided: {}'.format('yes' if collided else 'no')
        
        for layer in self.layers:
            layer.increment()
        
        return collided
    
    def delay(self, duration):
        #reset to initial state
        #run scanners without advancing packet
        #return self for ease of coding
        
        self.reset()
        
        for _ in range(duration):
            self.delay_one()
        
        return self
    
    def reset(self):
        self.packet_position = -1
        
        for i, layer in enumerate(self.layers):
            self.layers[i] = Layer(layer.size)
    
    def delay_one(self):
        for layer in self.layers:
            layer.increment()
    
    def any_collides(self):
        return any((self.increment() for _ in self.layers))
    
    @property
    def collides(self):
        return self.layers[self.packet_position].collides
    
    @property
    def severity(self):
        return sum((self.increment() * i * layer.size for i, layer in enumerate(self.layers)))


class Layer(object):
    def __init__(self, size):
        self.size = size
        self.scanner_position = 0 if size > 0 else None
        self.scanner_increment = 1 if size > 0 else None
    
    def __str__(self):
        if self.size == 0:
            return '...'
        else:
            return ' '.join(('[{}]'.format('S' if self.scanner_position == x else ' ') for x in range(self.size)))
    
    def increment(self):
        if self.size == 0:
            pass #intentional
        elif self.scanner_position == self.size - 1:
            self.scanner_position -= 1
            self.scanner_increment = -1
        elif self.scanner_position == 0:
            self.scanner_position += 1
            self.scanner_increment = 1
        else:
            self.scanner_position += self.scanner_increment
    
    @property
    def collides(self):
        return self.size != 0 and self.scanner_position == 0
