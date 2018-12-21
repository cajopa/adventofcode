class frozendict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            super().__setitem__(key, value)
    
    def __eq__(self, other):
        return super().__eq__(other)
    
    def __hash__(self):
        return hash(self.__class__) ^ hash(tuple(sorted(self.items(), key=lambda x: x[0])))
    
    def __repr__(self):
        return 'h' + super().__repr__()
    
    def update(self, other):
        for k,v in other.items():
            self[k] = v

### TODO: dict subclass that keys on an unadic function
#         should detect (somehow) changes in the "observed value"
#         a la knockout? (declare observable(s) and computed)
#         include caching
#         async
#         multiple keys returnable?
