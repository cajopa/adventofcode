from collections import defaultdict, Mapping
from copy import deepcopy
from itertools import product
import re


DEBUG = True

DEFAULT_INPUT = 'day21.input'
EXAMPLE_INPUT = 'day21.input.example'


def load(input_filename=DEFAULT_INPUT):
	with open(input_filename, 'r') as f:
		for line in (x.strip() for x in f):
			match = re.match(r'([\.#/]+) => ([\.#/]+)', line)
			
			if match:
				yield match.groups()

def run(input_filename, iterations):
	Grid.ENHANCEMENT_RULES = PatternCollection(load(input_filename))
	
	root_grid = Grid.initial()
	last_grid = None
	
	for i, last_grid in enumerate(root_grid):
		if DEBUG:
			print(i)
			print(last_grid, end='\n\n')
		
		if i == iterations:
			break
	
	return last_grid.count()

def run1():
	return run(DEFAULT_INPUT, 5)

def run2():
	return run(DEFAULT_INPUT, 18)

def run_example():
	return run(EXAMPLE_INPUT, 2)


class Grid:
	INITIAL_PATTERN = (False, True, False,
					  False, False, True,
					  True, True, True)
	
	ENHANCEMENT_RULES = None
	
	
	def __init__(self, flat_values):
		if isinstance(flat_values, Grid):
			other = flat_values #just rename for clarity
			self.size = other.size
			self.values = deepcopy(other.values)
		else:
			flat_values = list(flat_values)
			
			self.size = int(len(flat_values) ** 0.5)
			self.values = defaultdict(bool, zip(((x,y) for y in range(self.size) for x in range(self.size)), flat_values))
	
	def __iter__(self):
		current = self
		
		while True:
			yield current
			
			current = current.blit()
	
	def __eq__(self, other):
		return self.views & other.views
	
	def __hash__(self):
		return hash(self._hash_basis)
	
	def __str__(self):
		return '\n'.join(''.join(self.values[x,y] and '#' or '.' for x in range(self.size)) for y in range(self.size))
	
	__repr__ = __str__
	
	def __getitem__(self, key):
		return self.values[key]
	
	@property
	def _hash_basis(self):
		return tuple(min(self.views))
	
	@property
	def views(self):
		return set((self.flat(), self.rotate_clockwise(), self.rotate_counterclockwise(), self.rotate_halfturn(), self.reflect_horizontal(), self.reflect_vertical()))
	
	@classmethod
	def from_text(cls, text):
		return cls(x == '#' for x in text if x != '/')
	
	@classmethod
	def initial(cls):
		return cls(cls.INITIAL_PATTERN)
	
	######### basic operations #########
	
	def flat(self):
		return tuple([self.values[x,y] for y in range(self.size) for x in range(self.size)])
	
	def rotate_clockwise(self):
		return tuple([self.values[x,y] for x in range(self.size) for y in reversed(range(self.size))])
	
	def rotate_counterclockwise(self):
		return tuple([self.values[x,y] for x in reversed(range(self.size)) for y in range(self.size)])
	
	def rotate_halfturn(self):
		return tuple([self.values[x,y] for y in reversed(range(self.size)) for x in reversed(range(self.size))])
	
	def reflect_vertical(self):
		return tuple([self.values[x,y] for y in reversed(range(self.size)) for x in range(self.size)])
	
	def reflect_horizontal(self):
		return tuple([self.values[x,y] for y in range(self.size) for x in reversed(range(self.size))])
	
	######### problem-specific operations ##########
	
	def blit(self):
		subgrids = self.split(2 if self.size % 2 == 0 else 3)
		
		new_subgrids = {p: v.enhance() for p,v in subgrids.items()}
		
		return self.join(new_subgrids)
	
	def enhance(self):
		return self.ENHANCEMENT_RULES[self]
	
	def count(self):
		return sum(self.values.values())
	
	def split(self, subgrid_size):
		stripe_count = self.size // subgrid_size
		
		return {(X,Y): self.__class__(self.values[x,y] for y in range(Y*subgrid_size, (Y+1)*subgrid_size) for x in range(X*subgrid_size, (X+1)*subgrid_size)) for X,Y in product(range(stripe_count), repeat=2)}
	
	@classmethod
	def join(cls, subgrids):
		'requires a dict[x,y] = subgrid'
		
		stripe_count = max(subgrids.keys())[0] + 1
		subgrid_size = next(iter(subgrids.values())).size
		new_size = stripe_count * subgrid_size
		
		def subgrid_coord(x, y):
			return tuple(zip(divmod(x, subgrid_size), divmod(y, subgrid_size)))
		
		return cls(subgrids[sp][ssp] for sp, ssp in (subgrid_coord(x,y) for y in range(new_size) for x in range(new_size)))


class Pattern:
	def __init__(self, condition, result):
		self.condition = Grid(condition)
		self.result = Grid(result)
	
	def __eq__(self, other):
		return isinstance(other, Grid) and self.condition == other
	
	def __hash__(self):
		return hash(self._hash_basis)
	
	@property
	def _hash_basis(self):
		return self.condition._hash_basis
	
	@classmethod
	def from_text(cls, text_tuple):
		condition_text, result_text = text_tuple
		
		return cls(Grid.from_text(condition_text), Grid.from_text(result_text))


class PatternCollection(Mapping):
	def __init__(self, patterns):
		def inner(pattern):
			if isinstance(pattern, Pattern):
				return pattern
			elif isinstance(pattern, tuple):
				return Pattern.from_text(pattern)
			else:
				raise Exception('what the heck is this?')
		
		self.patterns = {inner(p) for p in patterns}
	
	def __getitem__(self, key):
		try:
			return next(p for p in self.patterns if p == key).result
		except StopIteration:
			raise KeyError(key)
	
	def __len__(self):
		return len(self.patterns)
	
	def __iter__(self):
		return iter(self.patterns)
