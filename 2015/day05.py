from itertools import izip, imap
import re

DEBUG = False

def load(input_filename):
    with open(input_filename, 'r') as f:
        for line in f:
            yield line.strip()

def run1(input_filename='input/day05'):
    return count_nice(load(input_filename), SantaString1)

def run2(input_filename='input/day05'):
    return count_nice(load(input_filename), SantaString2)

def count_nice(words, santa_string_class):
    return len([1 for x in words if santa_string_class(x).is_nice])


class SantaString1(object):
    prohibited_strings = ('ab', 'cd', 'pq', 'xy')
    
    def __init__(self, word):
        self.word = word
    
    @property
    def is_nice(self):
        return self.vowel_count >= 3 and self.has_double and not self.has_prohibited
    
    @property
    def vowel_count(self):
        return len([x for x in self.word if x in 'aeiou'])
    
    @property
    def has_double(self):
        return any(imap(lambda x: x[0] == x[1], izip(self.word[:-1], self.word[1:])))
    
    @property
    def has_prohibited(self):
        return any(((x in self.word) for x in self.prohibited_strings))


class SantaString2(object):
    def __init__(self, word):
        self.word = word
    
    @property
    def is_nice(self):
        return self.has_twice_pair and self.has_repeat_with_one_between
    
    @property
    def has_twice_pair(self):
        return bool(re.search(r'([a-z]{2}).*\1', self.word))
    
    @property
    def has_repeat_with_one_between(self):
        return bool(re.search(r'(.).\1', self.word))
