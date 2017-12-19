import re


DEBUG = False


class Node(object):
    registry = {}
    
    def __init__(self, name, children):
        self.name = name
        self._children = children
        self._parent = None
        
        self.registry[name] = self
    
    def __str__(self):
        return '{}({},{})'.format(self.__class__.__name__, self.name, self.weight, self.calculated_weight, len(self._children))
    
    @property
    def children(self):
        '''
        This is a bit funky - the childen might not exist yet, so they will either be strings (name) or Node objects.
        At first, they will all be strings. On access from this method, any that exist in the registry will be hydrated and stored.
        '''
        
        self._children = [x if isinstance(x, Node) else self.registry.get(x, x) for x in self._children]
        
        return {x.name: x for x in self._children}
    
    @property
    def parent(self):
        if not self._parent:
            for node in self.registry.itervalues():
                if self.name in node.children:
                    self._parent = node
        
        return self._parent
    
    @classmethod
    def populate(cls, node_params):
        for name, weight, children in node_params:
            cls(name, children)
    
    @classmethod
    def find_root(cls):
        current_node = next(cls.registry.itervalues())
        
        while current_node.parent:
            current_node = current_node.parent
        
        return current_node
    
    @classmethod
    def clear_registry(cls):
        cls.registry = {}

def load(input_filename):
    with open(input_filename, 'r') as f:
        for line in f:
            match = re.match(r'(?P<name>[a-z]+) \((?P<weight>\d+)\)(?: -> (?P<children>.+))?', line.strip())
            groupdict = match.groupdict()
            name = groupdict['name']
            weight = int(groupdict['weight'])
            children = [] if groupdict.get('children') is None else groupdict['children'].split(', ')
            
            yield name, weight, children
