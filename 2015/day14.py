import re


DEBUG=False
DEFAULT_INPUT = 'input/day14'
EXAMPLE_INPUT = 'input/day14.example'

DEFAULT_DURATION = 2503
EXAMPLE_DURATION = 1000


def load(input_filename=DEFAULT_INPUT):
    with open(input_filename, 'r') as f:
        for line in (x.strip() for x in f):
            match = re.match(r'(?P<name>[a-zA-Z]+) can fly (?P<speed>\d+) km/s for (?P<ontime>\d+) seconds, but then must rest for (?P<offtime>\d+) seconds.', line)
            
            if match:
                yield match.group('name'), int(match.group('speed')), int(match.group('ontime')), int(match.group('offtime'))

def run1():
    deer = {name: Reindeer(speed, ontime, offtime) for name, speed, ontime, offtime in load()}
    
    return max(map(lambda x: x.fly(DEFAULT_DURATION), deer.values()))

def run2(input_filename=DEFAULT_INPUT, duration=DEFAULT_DURATION):
    deer = {name: Reindeer(speed, ontime, offtime) for name, speed, ontime, offtime in load(input_filename)}
    
    points = dict.fromkeys(deer.keys(), 0)
     
    #inelegant and slow, but simple and should be fast enough
    for seconds in range(1, duration + 1):
        distances = {k: v.fly(seconds) for k,v in deer.items()}
        max_dist = max(distances.values())
        
        for i in (k for k,v in distances.items() if v == max_dist):
            points[i] += 1
    
    return max(points.values())


class Reindeer:
    def __init__(self, speed, ontime, offtime):
        self.speed = speed
        self.ontime = ontime
        self.offtime = offtime
    
    def fly(self, seconds):
        cycles, remainder = divmod(seconds, self.ontime + self.offtime)
        
        return (cycles * self.ontime + min(remainder, self.ontime)) * self.speed
