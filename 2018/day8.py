def load(input_filename):
    with open(input_filename, 'r') as f:
        return map(int, f.read().strip().split(' '))

def common_part(data=None, test=False):
    data = data or load('input/8.test' if test else 'input/8')
    
    return Node.parse(data)

def part1(data=None, test=False):
    '''
    What is the sum of all metadata entries?
    '''
    
    return common_part(data=data, test=test).checksum

def part2(data=None, workers=None, base_duration=None, test=False):
    '''
    '''
    

class Node:
    def __init__(self, *, metadata, children):
        self.metadata = metadata
        self.children = children
    
    @classmethod
    def parse(cls, stream):
        child_quantity = next(stream)
        metadata_quantity = next(stream)
        
        children = [cls.parse(stream) for _ in range(child_quantity)]
        metadata = [next(stream) for _ in range(metadata_quantity)]
        
        ### TODO: set parent
        
        return cls(metadata=metadata, children=children)
    
    @property
    def checksum(self):
        return sum(self.metadata) + sum(x.checksum for x in self.children)
