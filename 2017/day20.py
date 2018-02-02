from itertools import groupby
import re


DEBUG = True

DEFAULT_INPUT = 'day20.input'
EXAMPLE_PART1_INPUT = 'day20.input.example'
EXAMPLE_PART2_INPUT = 'day20.input.example.part2'


def load(input_filename=DEFAULT_INPUT):
    with open(input_filename, 'r') as f:
        for line in (x.strip() for x in f):
            match = re.match(r'p=<(?P<px>[- ]?\d+),(?P<py>[- ]?\d+),(?P<pz>[- ]?\d+)>, v=<(?P<vx>[- ]?\d+),(?P<vy>[- ]?\d+),(?P<vz>[- ]?\d+)>, a=<(?P<ax>[- ]?\d+),(?P<ay>[- ]?\d+),(?P<az>[- ]?\d+)>', line)
            
            if match:
                position = int(match.group('px')), int(match.group('py')), int(match.group('pz'))
                velocity = int(match.group('vx')), int(match.group('vy')), int(match.group('vz'))
                acceleration = int(match.group('ax')), int(match.group('ay')), int(match.group('az'))
                
                yield Particle(position, velocity, acceleration)

def run1(input_filename=DEFAULT_INPUT):
    particles = list(load(input_filename))
    
    for i in range(10000):
        for p in particles:
            p.blit()
    
    return min(((pn, p.distance_to_origin) for pn, p in enumerate(particles)), key=lambda x: x[1])

def run2(input_filename=DEFAULT_INPUT):
    particles = list(load(input_filename))
    
    def find_collisions():
        sort_func = lambda x: x[1].position
        for position, group in groupby(sorted(((pn, p) for pn, p in enumerate(particles)), key=sort_func), key=sort_func):
            grouped_particles = list(group)
            
            if len(grouped_particles) > 1:
                if DEBUG:
                    print('found collision at {}! removing particles {}'.format(position, ', '.join(map(str, (pn for pn,_ in grouped_particles)))))
                
                yield from (pn for pn,_ in grouped_particles)
    
    for i in range(100):
        if DEBUG:
            print('blit round {}'.format(i+1))
        
        for p in particles:
            p.blit()
        
        for pn in sorted(find_collisions(), reverse=True):
            del particles[pn]
    
    return len(particles)


class Particle:
    def __init__(self, position, velocity, acceleration):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
    
    def blit(self):
        self.velocity = tuple(map(sum, zip(self.velocity, self.acceleration)))
        self.position = tuple(map(sum, zip(self.position, self.velocity)))
    
    @property
    def distance_to_origin(self):
        return sum(map(abs, self.position))
