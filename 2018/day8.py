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
    The second check is slightly more complicated: you need to find the value of the root node
    The value of a node depends on whether it has child nodes.
    
    If a node has no child nodes, its value is the sum of its metadata entries. 
    
    However, if a node does have child nodes, the metadata entries become indexes which refer to
    those child nodes. A metadata entry of 1 refers to the first child node, 2 to the second, 3 to
    the third, and so on. The value of this node is the sum of the values of the child nodes
    referenced by the metadata entries. If a referenced child node does not exist, that reference is
    skipped. A child node can be referenced multiple time and counts each time it is referenced. A
    metadata entry of 0 does not refer to any child node.
    '''
    
    return common_part(data=data, test=test).value

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
    
    @property
    def value(self):
        if self.children:
            return sum(self.children[x-1].value for x in self.metadata if 0 <= x-1 < len(self.children))
        else:
            return sum(self.metadata)
