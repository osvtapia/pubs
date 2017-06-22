from UserDict import DictMixin

class OrderedDict(dict, DictMixin):

    def __init__(self, *args, **kwds):
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__end
        except AttributeError:
            self.clear()
        self.update(*args, **kwds)

    def clear(self):
        self.__end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.__map = {}                 # key --> [key, prev, next]
        dict.clear(self)

    def __setitem__(self, key, value):
        if key not in self:
            end = self.__end
            curr = end[1]
            curr[2] = end[1] = self.__map[key] = [key, curr, end]
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        key, prev, next = self.__map.pop(key)
        prev[2] = next
        next[1] = prev

    def __iter__(self):
        end = self.__end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.__end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def popitem(self, last=True):
        if not self:
            raise KeyError('dictionary is empty')
        if last:
            key = reversed(self).next()
        else:
            key = iter(self).next()
        value = self.pop(key)
        return key, value

    def __reduce__(self):
        items = [[k, self[k]] for k in self]
        tmp = self.__map, self.__end
        del self.__map, self.__end
        inst_dict = vars(self).copy()
        self.__map, self.__end = tmp
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)

    def keys(self):
        return list(self)

    setdefault = DictMixin.setdefault
    update = DictMixin.update
    pop = DictMixin.pop
    values = DictMixin.values
    items = DictMixin.items
    iterkeys = DictMixin.iterkeys
    itervalues = DictMixin.itervalues
    iteritems = DictMixin.iteritems

    def __repr__(self):
        '''
        This returns the dictionary as a string so people can see what's
        stored in the OrderedDict object.
        
        .. example: 
            >>> myDict = orderedDict.OrderedDict('one' = 1, 'two' = 2)
            >>> print myDict
            {'one':1, 'two':2}
        '''
        #get current keys and values
        keys = self.keys()
        values = self.values()
        
        #build you string to store keys:values
        _str = "{"
        if not keys or not values:
            return  '%s}' % _str
        
        for k,v in zip(keys, values):
            if k == keys[-1]:
                _str = "%s'%s' : %s}" % (_str,k, v)    
                break
            #end if
            
            _str = "%s'%s' : %s, " % (_str,k, v)
        #end loop
        
        return _str
    
    def add(self, key, value, index = None):
        '''
        adds a key:value pair to the dictionary based on index.
        If no index is passed in, then it will just add it to 
        the end of the key:value pairs lists
        
        @example:
            >>> myDict = orderedDict.OrderedDict('one' = 1, 'two' = 2)
            >>> myDict.add(key = 'three', value = 3)
            {'one':1, 'two':2, 'three' : 3}
            
        
        @example:
            >>> myDict = orderedDict.OrderedDict('one' = 1, 'two' = 2)
            >>> myDict.add(key = 'three', value = 3, index = 1)
            {'one':1, 'three' : 3, 'two':2}
        
        :param key: Name for the key in the dictionary
        :type key: str
        
        :param value: Value to go in the value for the key
        :type value: str | int | float | list | tuple | dict|
                     function | method | class 
        
        :param index: Position in the list of key:value pairs you want
                      your pair to be ordered.
        :type index: int
        '''
        #check if there are keys
        if self.keys():
            #get keys and values
            keys = self.keys()
            values = self.values()
            #if no key in self append key and value to end of lists
            if not self.has_key(key):
                #check length of keys against index
                if index > len(self.keys()):
                    keys.append(key)
                    values.append(value)
                #end if
            #end if
                else: 
                    keys.insert(index,key)
                    values.insert(index,value)
            #end if
            elif self.has_key(key):
                self.move(key, index)
                if value != self[key]:
                    self[key] = value
                return
            #clear self and rebuild in new order
            self.clear()
            for k,v in zip(keys, values):
                self[k] = v
            #end loops
        #end if
        else:
            self[key] = value
        #end else
        
    def move(self, key, index):
        '''
        This will move the key based on the input index argument
        
        :param key: Key value you want to reorder
        :type key: str
        
        :param index: Index in the self.keys() list where you would like you
                      key placed
        :type index: int
        '''
        if not self.has_key(key):
            raise KeyError('%s is not a valid key in %s' % (key, self))
        
        if self.keys():
            #get keys and values
            keys = self.keys()
            values = self.values()
        
        #get key and value from index
        originalIndex = keys.index(key)
        #pop key and value out of lists
        key = keys.pop(originalIndex)
        value = values.pop(originalIndex)
        #insert key and value into list
        keys.insert(index, key)
        values.insert(index, value)
        self.clear() #clear dict
        for k,v in zip(keys, values):
            self[k] = v

    def copy(self):
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d

    def __eq__(self, other):
        if isinstance(other, OrderedDict):
            if len(self) != len(other):
                return False
            for p, q in  zip(self.items(), other.items()):
                if p != q:
                    return False
            return True
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self == other
