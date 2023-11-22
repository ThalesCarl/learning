Dicts are everywhere in Python, because every python object has a `__builtins__.__dict__` that stores types, functions and embed objects.

Dicts are optimized and use hashtables as the engine for its performance. `set` and `frozenset` also use hashtables.

# Modern dict syntax

## Dict comprension

```python
dial_codes = [
    (880, 'Bangladesh'),
    (55,  'Brazil'),
    (86,  'China'),
    (91,  'India'),
    (62,  'Indonesia'),
    (81,  'Japan'),
    (234, 'Nigeria'),
    (92,  'Pakistan'),
    (7,   'Russia'),
    (1,   'United States'),
]
country_dial = {country: code for code, country in dial_codes}
reversed_dict = { code: country.upper()
                    for country, code in sorted(coutry_dial.items())
                    if code < 70 }
```

## Unpackgin dicts

I did not get this one:

```python
def dump(**kwargs):
    return kwargs

dump(**{'x': 1}, y=2, **{'z': 3})
# {'x': 1, 'y': 2, 'z': 3}
```

## Merging dicts with `|`

```python
d1 = {'a': 1, 'b': 3}
d2 = {'a': 2, 'c': 6}
d3 = d1 | d2 # d3 = {'a': 2, 'b': 3, 'c': 6}
d1 |= d2 # d1 = {'a': 2, 'b': 3, 'c': 6}
```

# Pattern matching with dicts

Dicts are supported by pattern matching as well as any mapping that is subclass of `collections.abc.Mapping`

```python
def get_creators(record: dict) -> list:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:
            return names
        case {'type': 'book', 'api': 1, 'author': name}:
            return [name]
        case {'type': 'book'}:
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {'type': 'movie', 'director': name}:
            return [name]
        case _:
            raise ValueError(f"Invalid record: {record!r}")
b1 = dict(api=1, author='Douglas Hofstadter', type='book', title='Gödel, Escher, Bach')
get_creators(b1) # [Douglas Hofstadter]
from collections import OrderedDict
b2 = OrderedDict(api=2, type='book',
        title='Python in a Nutshell',
        authors='Martelli Ravenscroft Holden'.split())
get_creators(b2) # ['Martelli', 'Ravenscroft', 'Holden']
```

The orders of the dict is irrelevant for pattern matching, even if the type is a OrderedDict.

Notice that that dict pattern matching works for partial matches, for example, the `title` is an extra argument that is not mentioned in the `case`, but it does not affect the matching. However, if you want to capture this values as a new dict to be used inside the case code, you can do that with an `**`

```python
food = dict(category='ice cream', flavor='vanilla', cost=199)
match food:
    case {'category': 'ice cream', **details}:
        print(f'Ice cream details: {details}')
```

# Mapping API

A dict has the interface in the two classes `abc.Mapping` and `abc.MutableMapping`. However, to personalize a dict is better to extend the `collections.UserDict` or use a `dict` with composition rather than using these `abc` base classes.

All these interfaces use a hash table, therefore, all of them have the same limitation, their keys must be hashable. The values dont have to be hashable, but the keys do.

A hashable object needs to have a `hash()` method and an `eq()` method that will match with any other equal object.

A hash of an object will change depending on the Python's version, the machine architecture and the salt added in the hash calculation. The hash of an object is only constant within a python process.

User defined objects are hashable by default, since its hash is their `id()` and the `__eq__()` method inhereted from `object` class will compares their ids. If you change the `__eq__()` method, make sure to also change the `__hash__()` method and make both of them depend only on immutable attributes of the object.

# Changing or inserting mutable values

See `example_4.py`

# Missing keys

If you dont want a dict to raise an error in case there is a missing key, you have two options: use a `defaultdict` or implement the `__missing__()` method in subclass of dict or any other mapping.

## Defaultdict

When you create a `collections.defaultdict`, you need to specify in the constructor what should the defaultdict do in case a missing key is provided. For example, `dd = defaultdict(list)` will have a `list()` method as the constructor. When you do `dd['new-key']` it will create a new list, insert it in the `dd` using `new-key` as key an return a reference to that list. 

Notice that a `defaultdict` will only work for places where the function `__getitem__()` is called, i. e., it will not work for `dd.get(k)` that still will return a `None` and `k in dd` will return `False`.

## `__missing__` method

See `missing_method.py`. Actually, the example is the opposite of what I was expecting. The example handles when a key is presented in number and string, but not if the key is missing. 

The `__missing__` method behaves differently whether you implement it on a `dict`, a `collections.UserDict` or a `abc.Mapping`. So be carefull with this.

# Dict variations

## `collections.OrderedDict`

Useful before python 3.6 when the order of a dict was not assured. Nowadays, it is used only for backward compatibility. However, there are some interesting differences. See the book for them.

## `collections.ChainMap`

It is a list of mappings and the key search is performed in the order of the list provided when constructing the chain. Moreover, new items are added only for the first dict of the chain

```python
d1 = dict(a=1, b=3)
d2 = dict(a=2, b=4, c=6)
from collections import ChainMap
chain = ChainMap(d1, d2)
chain['a'] # 1
chain['c'] # 6
chain['c'] = -1
d1 # {'a': 1, 'b': 3, 'c': -1}
d2 # {'a': 2, 'b': 4, 'c': 6}
```

## `collections.Counter`

A mapping that keeps a counter of the keys. It has the useful `most_common([n])` method that returns a ordered list of `n` elements most common.

```python
ct = collection.Counter('abracadabra')
print(ct) # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
ct.update('aaaaazzz')
print(ct) # Counter({'a': 10, 'z': 3, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
ct.most_common(3) # [('a', 10), ('z', 3), ('b', 2)]
```

## `shelve.Shelf`

A pickable dict that allows to store a key-value dict like it is a simple database. Keys must be `str` and the values must be also a object that the `pickle` module is able to serialize.

## `collections.UserDict`

It is always best to extend `collections.UserDict` rathen extending `dict` becuase the last one is intended to be more simple, which does not provides the same methods that the UserDict does. See `missing_method.py` to see the differences.

# Immutable mappings

In the standard library, all mappings are mutable. But if you want a kind of immutable solution you can use the `types.MappingProxyType` that doesnt allow item assignement to this "copy/proxy" of the object. However, if you modify the original object the proxy is modified as well

```python
from types import MappingProxyType
d = {1: 'A'}
d_proxy = MappingProxyType(d)
print(d_proxy) # mappingproxy({1: 'A'})
print(d_proxy[1]) # 'A'
d_proxy[2] = 'x' # Error: not allowed
d[2] = 'B'
print(d_proxy) # mappingproxy({1: 'A', 2: 'B'})
```