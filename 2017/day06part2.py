import itertools
import day06


DEBUG = False

def find_collision(initial_banks):
    old_bankses = {tuple(initial_banks): 0}
    old_banks = initial_banks
    
    if DEBUG:
        print initial_banks
    
    for rounds in itertools.count(1):
        new_banks = tuple(day06.reallocate(list(old_banks)))
        
        if DEBUG:
            print new_banks
        
        if new_banks in old_bankses:
            return rounds - old_bankses[new_banks]
        else:
            old_bankses[new_banks] = rounds
            old_banks = new_banks

run = lambda: day06.run(find_collision)
