from itertools import chain, groupby
import logging
import re


logging.basicConfig(level=logging.DEBUG)


def load(input_filename):
    with open(input_filename, 'r') as f:
        for line in (x.strip() for x in f):
            match = re.match(r'(?!<#)(\d+)/(\d+)', line)
            
            if match:
                yield match.groups()

def run1():
    connectors = [Connector(x,y) for x,y in load('day24.input')]
    
    best_path = max(Connector.walk(connectors), key=lambda x: Connector.score(x))
    best_score = Connector.score(best_path)
    
    logging.info('best ({1}): {0}'.format(map(str, best_path), best_score))
    
    return best_path, best_score

def run2():
    connectors = [Connector(x,y) for x,y in load('day24.input')]
    
    paths_by_length = {k: list(g) for k,g in groupby(sorted(Connector.walk(connectors), key=len), key=len)}
    import pdb; pdb.set_trace()
    max_path_length = max(paths_by_length.keys())
    best_longest_path = max(paths_by_length[max_path_length], key=Connector.score)
    best_score = Connector.score(best_longest_path)
    
    logging.info('best (score: {1}, length: {2}): {0}'.format(map(str, best_longest_path), best_score, max_path_length))
    
    return best_longest_path, max_path_length, best_score


class Connector:
    def __init__(self, side1, side2):
        self.side1 = int(side1)
        self.side2 = int(side2)
    
    def __eq__(self, other):
        return isinstance(other, Connector) and self.side1 == other.side1 and self.side2 == other.side2
    
    def __hash__(self):
        return hash(Connector) ^ hash((self.side1, self.side2))
    
    def __repr__(self):
        return 'Connector({}, {})'.format(self.side1, self.side2)
    
    def __str__(self):
        return '{:02d}/{:02d}'.format(self.side1, self.side2)
    
    @property
    def reversed(self):
        try:
            return ReversedConnector(self)
        except SymmetricConnectorError:
            pass
    
    @classmethod
    def walk(cls, connectors):
        connector_map = cls._make_map(connectors)
        
        # #loop through all connectors as first links
        # for connector in connectors:
        #     yield from connector._walk(connector_map)
        #loop through all connectors with a zero side as first links
        for connector in (x for x in connectors if 0 in (x.side1, x.side2)):
            yield from connector._walk(connector_map)
    
    @classmethod
    def score(cls, path):
        return sum(x.side1 + x.side2 for x in path)
    
    @classmethod
    def _make_map(cls, connectors):
        connectors = list(connectors)
        reversed_connectors = [y for y in (x.reversed for x in connectors) if y]
        
        def group(connectors):
            return groupby(sorted(connectors, key=lambda x: x.side1), key=lambda x: x.side1)
        
        #create map of connectors, including reversed links when a!=b
        connector_map = dict((k,list(g)) for k,g in group(connectors))
        
        for k,g in group(reversed_connectors):
            connector_map.setdefault(k, []).extend(g)
        
        logging.debug(connector_map)
        
        return connector_map
    
    def _walk(self, connector_map, previous=tuple()):
        path = previous + (self,)
        
        logging.debug(' '.join(map(str, path)))
        
        #find all connectors that match appropriately without looping
        #TODO: including the reversed - needs to not self-loop!
        #        ReversedConnector(x) == x
        eligible_next_connectors = set(connector_map.get(self.side2, [])) - set(path)
        
        #continue walking if possible, and only yield once there is nowhere to go
        # if there are any more possible connectors, the score will be higher than without
        for downstream_connector in eligible_next_connectors:
            yield from downstream_connector._walk(connector_map, previous=path)
        else:
            yield path


class ReversedConnector(Connector):
    def __init__(self, other):
        if getattr(other, 'other', None):
            raise DoubleReverseError
        
        if other.side1 == other.side2:
            raise SymmetricConnectorError
        
        super().__init__(other.side2, other.side1)
        
        self.other = other
    
    def __eq__(self, other):
        return self.other == other
    
    def __hash__(self):
        return hash(self.other)
    
    def __repr__(self):
        return 'ReversedConnector({0.side1}, {0.side2}, other={0.other})'.format(self)
    
    def __str__(self):
        return r'{:02d}\{:02d}'.format(self.side2, self.side1)


class BaseError(Exception):
    pass

class DoubleReverseError(BaseError):
    def __init__(self):
        super().__init__('Reversing an already-reversed connector is dumb')

class SymmetricConnectorError(BaseError):
    def __init__(self):
        super().__init__('There is no point in reversing a symmetric connector')
