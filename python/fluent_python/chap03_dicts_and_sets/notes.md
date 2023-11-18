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