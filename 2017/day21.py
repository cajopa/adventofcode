from collections import defaultdict, Mapping
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



class Linear2DArray(Mapping):
	def __init__(self, width, flat_values):
		self.width = width
		
		self.values = list(flat_values)
	
	def __getitem__(self, key):
		x,y = key
		
		try:
			return self.values[y*self.width + x]
		except IndexError:
			return None
	
	def __setitem__(self, key, value):
		x,y = key
		
		if x >= self.width:
			raise KeyError('x is out of bounds')
		
		self.values[y*self.width + x] = value
	
	def __iter__(self):
		return iter(self.values)
	
	def __len__(self):
		return len(self.values)
	
	def copy(self):
		return self.__class__(self.width, self.values)


###### FIXME: refactor to use Linear2DArray code properly
class Grid(Linear2DArray):
	INITIAL_PATTERN = (False, True, False,
					  False, False, True,
					  True, True, True)
	
	ENHANCEMENT_RULES = None
	
	
	def __init__(self, flat_values):
		if isinstance(flat_values, Grid):
			other = flat_values #just rename for clarity
			
			super(Grid, self).__init__(other.width, other.values.copy())
		else:
			flat_values = list(flat_values)
			
			width = int(len(flat_values) ** 0.5)
			
			super(Grid, self).__init__(width, flat_values)
	
	def __iter__(self):
		#NOTE: completely changes the meaning
		
		current = self
		
		while True:
			yield current
			
			current = current.blit()
	
	def __eq__(self, other):
		return self.views & other.views
	
	def __hash__(self):
		return hash(self._hash_basis)
	
	def __str__(self):
		return '\n'.join(''.join(self[x,y] and '#' or '.' for x in range(self.width)) for y in range(self.width))
	
	__repr__ = __str__
	
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
		return tuple([self[x,y] for y in range(self.width) for x in range(self.width)])
	
	def rotate_clockwise(self):
		return tuple([self[x,y] for x in range(self.width) for y in reversed(range(self.width))])
	
	def rotate_counterclockwise(self):
		return tuple([self[x,y] for x in reversed(range(self.width)) for y in range(self.width)])
	
	def rotate_halfturn(self):
		return tuple([self[x,y] for y in reversed(range(self.width)) for x in reversed(range(self.width))])
	
	def reflect_vertical(self):
		return tuple([self[x,y] for y in reversed(range(self.width)) for x in range(self.width)])
	
	def reflect_horizontal(self):
		return tuple([self[x,y] for y in range(self.width) for x in reversed(range(self.width))])
	
	######### problem-specific operations ##########
	
	def blit(self):
		subgrids = self.split(2 if self.width % 2 == 0 else 3)
		
		new_subgrids = {p: v.enhance() for p,v in subgrids.items()}
		
		return self.join(new_subgrids)
	
	def enhance(self):
		return self.ENHANCEMENT_RULES[self]
	
	def count(self):
		return sum(self.values)
	
	def split(self, subgrid_width):
		stripe_count = self.width // subgrid_width
		
		return {(X,Y): self.__class__(self[x,y] for y in range(Y*subgrid_width, (Y+1)*subgrid_width) for x in range(X*subgrid_width, (X+1)*subgrid_width)) for X,Y in product(range(stripe_count), repeat=2)}
	
	@classmethod
	def join(cls, subgrids):
		'requires a dict[x,y] = subgrid'
		
		stripe_count = max(subgrids.keys())[0] + 1
		subgrid_width = next(iter(subgrids.values())).width
		new_size = stripe_count * subgrid_width
		
		def subgrid_coord(x, y):
			return tuple(zip(divmod(x, subgrid_width), divmod(y, subgrid_width)))
		
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
