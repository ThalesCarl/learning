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
