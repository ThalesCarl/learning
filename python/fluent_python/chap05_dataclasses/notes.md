# General idea of dataclasses

First take a look of using a regular class to represent some data

```python
class Coordinate:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

moscow = Coordinate(55.76, 37.62)
print(moscow) # Cordinate object at 0x0000001 - not useful
another_coord = Coordinate(55.76, 37.62)
another_coord == moscow # False, because the __eq__ compares objects ids instead of attributes
```

All the dataclasses seen in this chapter will provide the `__init__`, `__repr__` and `__eq__` automatically. None of them use inheritance to work.

## Using `collections.namedtuple`

```python
from collections import namedtuple
Coordinate = namedtuple('Coordinate', 'lat lon')
moscow = Coordinate(55.756, 37.617)
print(moscow) # Coordinate(lat=55.756, lon=37.617)
moscow == Coordinate(lat=55.756, lon=37.617) # True - way better
```

## Using `typing.NamedTuple`

```python
from typing import NamedTuple
Coordinate = NamedTuple('Coordinate', lat=float, lon=float)
moscow = Coordinate(55.756, 37.617)
moscow == Coordinate(lat=55.756, lon=37.617) # True

# Since python 3.6, you can also do:

# notice that we are not inhereting from NamedTuple, but from tuple directly
class Coordinate(NamedTuple):
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'
```

## Using `dataclasses.dataclass` (or just `@dataclass` in this notes)

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float
```

# Differences between the three dataclasses

|         attribute           | namedtuple         | NamedTuple         | dataclass |
| --------------------------- | ------------------ | -----------        | ------    |
| mutable instances           | No                 | No                 | Yes (but can be No if you use the frozen parameter) |
| Use PEP 526 syntax          | No                 | Yes                | Yes |
| dict creation            | x._asdict()       | x._asdict()       | dataclasses.asdict(x) |
| get names of the fields           | x._fields         | x._fields         | [f.name for f in dataclasses.fields(x)] |
| get default values              | x._field_defaults | x._field_defaults | [f.default for f in dataclasses.fields(x)] |
| get fields types           | N/A               | x.&#x5f;&#x5f;annotations&#x5f;&#x5f; | x.&#x5f;&#x5f;annotations&#x5f;&#x5f; |
| new instance with changes | x._replace(…)     | x._replace(…)     | dataclasses.replace(x, …) |
| new class during execution  | namedtuple(…)     | NamedTuple(…)     | dataclasses.make_dataclass(…) |

# Classic named tuples

A `collections.namedtuple` is a tuple that have a name for itself for its parameters within. 

The namedtuple has the same memory as a normal tuple because the names are stored in the class definition.

You can use the `defaults` kwarg to fill the arguments from right to left.

```python
Coordinate = namedtuple('Coordinate', 'lat lon reference', defaults=['WGS84'])
somewhere = Coordinate(0, 0)
print(somewhere) # Coordinate(lat=0, lon=0, reference='WGS84')
```

# Named tuples with types

The only difference between a `collections.namedtuple` and a `typing.NamedTuple` is the type annotations that are store in the `__annotation__` attribute.

The annotations must follow the PEP 484 that states that the acceptable type hints are:
- a concrete class, like `str` or `FrenchDeck` (user defined function from chap01)
- a parametrized collection, like `list[int]`, `tuple[str, float]`
- `typing.Optional` that is used when a field might be `None`

You can pass the default value using the syntax `var_name: type_hint = default_value`. Example:

```python
# Notice for now that is not a NamedTuple yet
class DemoPlainClass:
    a: int
    b: float = 1.1
    c = 'spam'

print(DemoPlainClass.__annotations__) # {'a': <class 'int'>, 'b': <class 'float'>} - c has no type hint, so it's not stored here
print(DemoPlainClass.a) # `a` is discarded because has no default value
print(DemoPlainClass.b) # 1.1
print(DemoPlainClass.c) # 'spam'

# Now using the NamedTuple
from typing import NamedTuple
class DemoNTClass(NamedTuple):
    a: int
    b: float = 1.1
    c = 'spam'

print(DemoPlainClass.__annotations__) # {'a': <class 'int'>, 'b': <class 'float'>} - same as before
print(DemoPlainClass.a) # <_collections._tuplegetter object at 0x101f0f940> - 
print(DemoPlainClass.b) # <_collections._tuplegetter object at 0x101f0f8b0>
print(DemoPlainClass.c) # 'spam'
nt = DemoNTClass(8) # DemoNTClass(a=8, b=1.1)
nt.c = 'eggs' # Error: 'c' is read-only
nt.b = 1.2 # Error: can't set attribute

# Now using dataclass
from dataclasses import dataclass

@dataclass
class DemoDataClass:
    a: int
    b: float = 1.1
    c = 'spam'
print(DemoDataClass.__annotations__) # {'a': <class 'int'>, 'b': <class 'float'>} - same as before
print(DemoDataClass.a) # Error: no attribute a
print(DemoDataClass.b) # 1.1
print(DemoDataClass.c) # 'spam'
dc = DemoNTClass(9) # DemoNTClass(a=9, b=1.1)
dc.c = 'eggs' # no error because this dataclass is not frozen
dc.b = 1.2 # no errors and no type verification at runtime
dc.z
```

# The dataclass details

The @dataclass decorator has the following signature:

```python
@dataclass(*, init=True, repr=True, eq=True, order=False,
              unsafe_hash=False, frozen=False)
```

From here, you would probably change just:
  - `order=True` that allows the ordering by generating the `__lt__`, `__le__`, `__gt__` and `__ge__` methods
  - `frozen=True` that makes the class immutable

You can use the syntax above to use default values, but beware that after the first one field with a default value, all of them must have a default value as well, because the decorator will generate the `__init__` function.

Beware with default values that uses a collection. Even the definition below is not allowed in order to prevent bugs

```python
@dataclass
class ClubMember:
    name: str
    guests: list = [] # Probably would cause bug

# Use this instead
from dataclasses import dataclass, field

@dataclass
class ClubMember:
    name: str
    guests: list = field(default_factory=list) # It will generate one list for each instance of Club Member
    guests: list[str] = field(default_factory=list) # Since python 3.9, we can annotate the type of the list as well, before that we would need to use typing.List to do this
```

## Post init method

See `hackerclub.py` to see a example on how to use the `__post_init__()` function to execute code even after the generated `__init__()` have been run.

## dataclass caveats

### ClassVar

If you have a class variable inside a dataclass, mypy will produce an error unless you use `typing.ClassVar`. So, the example on the `hackerclub.py` becomes

```python
class HackerClubMember(ClubMember):
    # the typing means that all_handles is a class attribute of type set of string, with a empty set as default value
    all_handles: ClassVar[set[str]] = set()
```

### InitVar

```python
@dataclass
class C:
    i: int
    j: int | None = None
    database: InitVar[DatabaseType | None] = None

    def __post_init__(self, database):
        if self.j is None and database is not None:
            self.j = database.lookup('j')

c = C(10, database=my_database)
```

Because the type is `InitVar`, the database field will not be treated as a regular field and it will only be available for the `__init__` and `__post_init__` functions.

# Dataclasses as code smeels

If you use too much dataclasses, it could mean your code is bad structured because the its functionality is outside the class. But there are places where a dataclass makes sence:
- A sketch of a new object
- A intermediate representation that will be used for communication with an API

# Pattern matching of dataclasses

There is three types of pattern matching with classes (in general, not just dataclasses): simple, named and positional.

## Simple

For builtin objects (bool, bytearray, bytes, dict, float, frozenset, int, list, set, str, tuple) the following should be used
```python
match x:
    case float():
        do_something_with(x)

    # DANGER, because float would be created as variable that matches anything instead of checking the type
    case float:
        do_something_with(x)
```

Question: why they did it like that?

## Named

```python
import typing

class City(typing.NamedTuple):
    continent: str
    name: str
    country: str

cities = [
    City('Asia', 'Tokyo', 'JP'),
    City('Asia', 'Delhi', 'IN'),
    City('North America', 'Mexico City', 'MX'),
    City('North America', 'New York', 'US'),
    City('South America', 'São Paulo', 'BR'),
]

def match_asian_cities():
    results = []
    for city in cities:
        match city:
            # match any instance that has continent == 'Asia'
            case City(continent='Asia'):
                results.append(city)
    return results

def match_asian_countries():
    results = []
    for city in cities:
        match city:
            # Creates the variable cc (could it be country also) to be used inside the scope
            case City(continent='Asia', country=cc)
                results.append(country)
    return results
```

## Positional

This type uses the position of the arguments in the declaration of the function

```python
def match_asian_cities_positional():
    results = []
    for city in cities:
        match city:
            # check if first attribute is 'Asia'
            case City('Asia'):
                results.append(city)
            # Suppose this is in another example
            # Match the first attribute and create a variable to be used in the scope
            case City('Asia', _, country):
                print(country)
                
    return results
```

The positional matching uses the `__match_args__` generated by the `typing.NamedTuple`. This will be see in more detail on chapter 11.

