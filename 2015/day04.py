from hashlib import md5
import itertools


DEBUG = False
INPUT = 'bgvyzdsv'


def run1():
    return find_first_good(INPUT)

def run2():
    return find_first_good(INPUT, 6)

def is_hash_good(secret, counter, required_zeroes):
    return md5(''.join(map(str, [secret, counter]))).hexdigest().startswith('0'*required_zeroes)

def find_first_good(secret, required_zeroes=5):
    for i in itertools.count():
        if is_hash_good(secret, i, required_zeroes):
            return i
