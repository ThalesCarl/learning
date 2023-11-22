class StrKeyDict0(dict):
    """
    Emulates the processing of the ports of an Arduino board 
    """
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()

import collections
class StrKeyDict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]
    
    def __contains__(self, key: object) -> bool:
        return str(key) in self.data
    
    def __setitem__(self, key: Any, item: Any) -> None:
        self.data[str(key)] = item


d = StrKeyDict0([('2', 'two'), ('4', 'four')])
print(d['4'])