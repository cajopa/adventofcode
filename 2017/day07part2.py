from day07 import Node, load


DEBUG = False


class WeightedNode(Node):
    def __init__(self, name, weight, children):
        self.weight = weight
        
        super(WeightedNode, self).__init__(name, children)
    
    def __str__(self):
        return '{}({},{} ({}),{})'.format(self.__class__.__name__, self.name, self.weight, self.calculated_weight, len(self._children))
    
    @classmethod
    def populate(cls, node_params):
        for name, weight, children in node_params:
            cls(name, weight, children)
    
    @property
    def is_balanced(self):
        if self.children:
            children_iter = self.children.itervalues()
            goal = next(children_iter).calculated_weight
            
            return all((x.calculated_weight == goal for x in children_iter))
        else:
            return True
    
    @property
    def calculated_weight(self):
        return self.weight + sum((x.calculated_weight for x in self.children.itervalues()))
    
    def find_unbalanced(self):
        '''
        Follow the unbalanced branch until all children are balanced (current only has leaves).
        '''
        
        if DEBUG:
            print '{}.find_unbalanced'.format(self.name)
        
        if self.is_balanced:
            if DEBUG:
                print '  is balanced'
                print '  returning'
            
            return None
        else:
            if DEBUG:
                print '  not balanced'
                print '  finding in children'
            
            for child in self.children.itervalues():
                if DEBUG:
                    print '    trying {}...'.format(child.name)
                
                maybe_return = child.find_unbalanced()
                
                if maybe_return:
                    if DEBUG:
                        print 'bingo!'
                    
                    return maybe_return
            
            if DEBUG:
                print '  returning myself ({})'.format(self.name)
            
            return self

def run(filename=None):
    WeightedNode.clear_registry()
    WeightedNode.populate(load(filename or 'day07.input'))
    
    unbalanced_node = WeightedNode.find_root().find_unbalanced()
    
    #use modified median because if there are two children and the node is unbalanced, the change in weight is undefined
    child_weights = [x.calculated_weight for x in unbalanced_node.children.itervalues()]
    target_weight = list(sorted(child_weights))[len(child_weights)/2]
    problem_child = [x for x in unbalanced_node.children.itervalues() if x.calculated_weight != target_weight][0]
    
    if DEBUG:
        print 'child weights: {!r}'.format(child_weights)
        print 'target weight: {}'.format(target_weight)
        print 'problem child: {!s}'.format(problem_child)
    
    return problem_child.weight - (problem_child.calculated_weight - target_weight), unbalanced_node
