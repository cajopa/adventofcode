from itertools import izip


DEBUG = False
DEFAULT_INPUT = 'hxbxwxba'


def run1(initial=DEFAULT_INPUT):
    return str(SantaPassword(initial, (rule_straight, rule_bad_letters, rule_two_pairs)).next_good)

def run2(initial=DEFAULT_INPUT):
    return str(SantaPassword(initial, (rule_straight, rule_bad_letters, rule_two_pairs)).next_good.next_good)


class SantaPassword(object):
    def __init__(self, initial, rules):
        self.value = [ord(x)-ord('a') for x in initial]
        self.rules = rules
    
    def __str__(self):
        return ''.join((chr(x+ord('a')) for x in self.value))
    
    def __contains__(self, value):
        if isinstance(value, str):
            return (ord(value) - ord('a')) in self.value
    
    def increment(self):
        #ripple add is slow but understandable
        for i,v in izip(xrange(len(self.value)-1, -1, -1), reversed(self.value)):
            if v == 25:
                self.value[i] = 0
            else:
                self.value[i] += 1
                break
        
        if DEBUG:
            print 'incremented to: {}'.format(str(self))
        
        return self
    
    @property
    def next_good(self):
        while True:
            if self.increment().is_good:
                return self
    
    @property
    def is_good(self):
        return all((rule(self) for rule in self.rules))


def rule_straight(self):
    return any((a == b - 1 == c - 2 for a,b,c in izip(self.value, self.value[1:], self.value[2:])))

def rule_bad_letters(self):
    return not ('i' in self or 'o' in self or 'l' in self)

def rule_two_pairs(self):
    return len(set((a for a,b in izip(self.value, self.value[1:]) if a == b))) >= 2
