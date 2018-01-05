from functools import partial
from itertools import chain, imap


DEBUG = False


DEFAULT_INPUT = '1113222113'
EXAMPLE_INPUT = '1'


def rle(sequence):
    sequence_iter = iter(sequence)
    last = next(sequence_iter)
    count = 1
    
    for i in chain(sequence_iter, [None]):
        if i != last:
            yield (count, last)
            last = i
            count = 1
        else:
            count += 1

def lookandsay(rle_sequence):
    return chain.from_iterable(rle_sequence)

def last(sequence):
    to_return = None
    
    for i in sequence:
        to_return = i
    
    return to_return

def _run1(initial=DEFAULT_INPUT, runs=40):
    last = initial
    
    for i in range(runs):
        last = ''.join(imap(str, lookandsay(rle(last))))
        yield last

def run(initial=DEFAULT_INPUT, runs=40):
    return len(last(_run1(initial=initial, runs=runs)))

run1 = partial(run, runs=40)
run2 = partial(run, runs=50)
