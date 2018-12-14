from math import ceil


def eratosthenes(max_number):
    to_return = [None, None] + list(range(2, max_number+1))
    current = 2
    
    while current <= ceil(max_number**0.5):
        for i in range(current*2, max_number+1, current):
            to_return[i] = None
        
        try:
            current = next(x for x in to_return if x is not None and x > current)
        except StopIteration:
            break
    
    return list(filter(None, to_return))

def factorize(number):
    to_return = []
    primes = eratosthenes(int(ceil(number**0.5)))
    start_at = 0
    
    while True:
        found_one = False
        
        for i,prime in enumerate(primes[start_at:]):
            if number % prime == 0:
                to_return.append(prime)
                start_at += i
                number //= prime
                found_one = True
                break
        
        if not found_one:
            if number != 1:
                to_return.append(number)
            break
    
    return to_return
