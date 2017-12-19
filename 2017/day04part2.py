from frozendict import frozendict


class Word(object):
    def __init__(self, letters):
        self.letter_stats = {}
        
        for letter in letters:
            if letter in self.letter_stats:
                self.letter_stats[letter] += 1
            else:
                self.letter_stats[letter] = 1
    
    def __eq__(self, other):
        return isinstance(other, Word) and self.letter_stats == other.letter_stats
    
    def __hash__(self):
        return hash(frozendict(self.letter_stats))

class Phrase(object):
    def __init__(self, words):
        self.words = words
    
    @classmethod
    def from_string(cls, string):
        words = []
        
        for word_letters in string.strip().split(' '):
            words.append(Word(word_letters))
        
        return cls(words)
    
    @property
    def is_valid(self):
        return len(self.words) == len(set(self.words))

def count_valid(input_filename):
    count = 0
    
    with open(input_filename, 'r') as f:
        for line in f:
            if Phrase.from_string(line).is_valid:
                count += 1
    
    return count
