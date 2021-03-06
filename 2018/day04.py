from collections import Counter
from itertools import chain
import re


BEGIN_SHIFT = object()
WAKE_UP = object()
FALL_ASLEEP = object()


def load(input_filename):
    pattern = re.compile(r'\[(?P<year>\d{4})-(?P<month>\d\d)-(?P<day>\d\d) (?P<hour>\d\d):(?P<minute>\d\d)\] (?P<action>Guard #(?P<guard_id>\d+) begins shift|wakes up|falls asleep)')
    
    with open(input_filename, 'r') as f:
        for line in f:
            match = pattern.match(line.strip())
            
            if match.group('action').endswith('begins shift'):
                act = BEGIN_SHIFT
            elif match.group('action') == 'wakes up':
                act = WAKE_UP
            elif match.group('action') == 'falls asleep':
                act = FALL_ASLEEP
            
            yield {
                'date': (
                    int(match.group('year')),
                    int(match.group('month')),
                    int(match.group('day')),
                ),
                'time': (
                    int(match.group('hour')),
                    int(match.group('minute')),
                ),
                'act': act,
                'guard_id': match.group('guard_id') and int(match.group('guard_id')),
            }

def part1():
    guards = _parse_input_stream(load('input/4'))
    
    #find the sleepiest guard
    sleepiest_guard = max(guards.values(), key=lambda x: x.total_sleep_time)
    
    return sleepiest_guard.id * sleepiest_guard.sleepiest_minute

def part2():
    guards = _parse_input_stream(load('input/4'))
    
    #find the sleepiest sleepiest minute
    sleepiest_guard = max(guards.values(), key=lambda x: len(x.minutes_by_sleepiness) and x.minutes_by_sleepiness.most_common(1)[0][1])
    
    return sleepiest_guard.id * sleepiest_guard.sleepiest_minute

def _parse_input_stream(data):
    #sort so actions have correct referents
    sorted_actions = sorted(data, key=lambda x: (x['date'], x['time']))
    
    #chintzy state machine to parse action stream
    guards = {}
    current_guard = None
    for action in sorted_actions:
        if action['act'] is BEGIN_SHIFT:
            current_guard = guards.setdefault(action['guard_id'], Guard(action['guard_id']))
        elif action['act'] is FALL_ASLEEP:
            current_guard.sleep(action['time'])
        elif action['act'] is WAKE_UP:
            current_guard.waken(action['time'])
    
    return guards


class Guard:
    def __init__(self, id_):
        self.id = id_
        self.asleep_ranges = []
        
        self.asleep_time = None
    
    def __repr__(self):
        return f'<{self.__class__.__name__} id:{self.id}>'
    __str__=__repr__
    
    @property
    def total_sleep_time(self):
        return sum(len(list(x)) for x in self.asleep_ranges)
    
    @property
    def sleepiest_minute(self):
        return self.minutes_by_sleepiness.most_common(1)[0][0]
    
    @property
    def minutes_by_sleepiness(self):
        return Counter(chain.from_iterable(self.asleep_ranges))
    
    def sleep(self, time):
        self.asleep_time = time
    
    def waken(self, time):
        self.asleep_ranges.append(range(self.asleep_time[1], time[1]))
        self.asleep_time = None
