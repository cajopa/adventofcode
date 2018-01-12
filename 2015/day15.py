import re
from itertools import product
from functools import reduce


DEBUG=False
DEFAULT_INPUT = 'input/day15'
EXAMPLE_INPUT = 'input/day15.example'

DEFAULT_TOTAL_AMOUNT = 100


def load(input_filename=DEFAULT_INPUT):
    with open(input_filename, 'r') as f:
        for line in (x.strip() for x in f):
            match = re.match(r'(?P<name>[a-zA-Z]+): capacity (?P<capacity>-?\d+), durability (?P<durability>-?\d+), flavor (?P<flavor>-?\d+), texture (?P<texture>-?\d+), calories (?P<calories>-?\d+)', line)
            
            if match:
                capacity = int(match.group('capacity'))
                durability = int(match.group('durability'))
                flavor = int(match.group('flavor'))
                texture = int(match.group('texture'))
                calories = int(match.group('calories'))
                
                yield Ingredient(match.group('name'), capacity, durability, flavor, texture, calories)

def run1():
    return max(Recipe(DEFAULT_TOTAL_AMOUNT, list(load())))

def run2():
    pass


class Ingredient:
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories


class Recipe:
    def __init__(self, total_amount, ingredients):
        self.total_amount = total_amount
        self.ingredients = ingredients
    
    def __iter__(self):
        for amounts in self.permute_amounts(self.total_amount, len(self.ingredients)):
            yield self.score(amounts), amounts
    
    def score(self, amounts):
        trait_scores = [max(0, sum((x*y for x,y in zip(amounts, (getattr(z, trait) for z in self.ingredients))))) for trait in ('capacity', 'durability', 'flavor', 'texture')]
        return reduce(lambda x,y: x*y, trait_scores)
    
    @staticmethod
    def permute_amounts(total, count):
        if count == 1:
            yield (total,)
        else:
            for i in range(1, total+1):
                yield from filter(lambda x: 0 not in x, ((x,) + y for x,y in product([i], permute_amounts(total-i, count-1))))
