This chapter is about using type hints for functions. For instance, the function below receives a `str` an return a list of `str`.

```python
def tokenize(s: str) -> list[str]:
    return s.replace('(', ' ( ').replace(')', ' ) ').split()
```

# Gradual type checking

Python type system is gradual, which means:
- It's optional: the type verifier doesn't say anything if a type is not provided by default. It assumes `Any` if cannot identify which type a object is.
- Do not capture typing errors during runtime
- Do not improve performance: even thought type hints provide information that might be used for optimization, for now they are not used yet.

See a usage example in the `type_hints_practice.py` file.

# Types classification

- Nominal typing: Objects and variables have types, but objects only exists during execution. Because of this, a type error might arise from the code static analysis.
- Duck typing: objects have types, but variables (including parameters don't). This means that a object type does not matter, as long as the operations that the object need are supported.

```python
class Bird:
    pass

class Duck(Bird):
    def quack(self):
        print('Quack!')

def alert(birdie):
    birdie.quack()

def alert_duck(birdie: Duck) -> None:
    birdie.quack()

def alert_bird(birdie: Bird) -> None:
    birdie.quack()

daffy = Duck()
alert(daffy)       # No problem
alert_duck(daffy)  # No problem
alert_bird(daffy)  # No problem for python, but problem for mypy, because daffy is a Duck, but not a Bird. However, for python, since Duck is subclass of Bird, it does not have a problem with it.

woody = Bird()
alert(woody) # Python problem: Bird has no attribute quack
alert_duck(woody) # Mypy problem: argument 1 to alert_duck has incompatible type Bird, expected Duck
alert_bird(woody)
```

# Types used in type hints

Almost every type in python can be used in the type annotations, but there are restrictions and recommendations.

## `Any`

The basic type that is assumed by the type verifier. This means that if the verifier see `def double(x)` it will assume `def double(x: Any) -> Any`. We assume that `Any` can be used in any operation.

Remember to discuss with the guys about the consistency point.

Consistent-with rules:

1. Given types T1 and subtype T2, T2 is consistent-with T1 (Liskov substitution)
2. Every type is consistent-with `Any`: you can pass objects of any type ina argument declared with the type `Any`
3. `Any` is consistent-with every type: you can always pass a object of type `Any` to a function that expects any other type.

## Simple types and classes

Any base type such as `int`, `float`, `str` and `bytes` can be used in the typing annotation, as well as concrete classes from the standard lib or classes defined by the user.

A class is consistent-with all of its superclasses

## `Optional` and `Union`

`Optional[some_type]` is used when the default value of an argument is `None`.

A `Union[type1, type2]` means that a argument can be of `type1` **or** `type2`

The syntax `Optional[some_type]` is a alias to `Union[some_type, None]`

Since Python 3.10 the notation `x: type1 | type2` is preferable instead of `Union[type1, type2]`

If possible, avoid creating a function that returns a Union, because it demands extra effort from the user.

`Union[A, B, Union[C, D, E]]` is the same as `Union[A, B, C, D, E]`

## Generic collections

Even tough you can store anything in a sequence such as a list. In general, we use a list of type that have a common operation.

```python
def tokenize(text: str) -> list[str]:
    return text.upper().split()
```

`stuff: list` and `stuff: list[Any]` is the same.

An `array.array` is yet not fully supported by type hints, because you pass the type in the creation of it.

## Tuples

### Tuples as registers

Use `tuple[A, B, C]`. For example:

```python
from geolib import geohash as gh

def geohash(lat_lon: tuple[float, float]) -> str:
    return gh.encode(*lat_lon)
```

### Tuples with named fields

Use `typing.NamedTuple` as seen before

### Tuples as immutable sequences

For tuples of unknown size, use `tuple[some_type, ...]`.

`stuff: tuple[Any, ...]` and `stuff: tuple` are equivalent.

```python
from collections.abc import Sequence

def columnize(sequence: Sequence[str], num_columns: int = 0) -> list[tuple[str, ...]]:
    if num_columns == 0:
        num_columns = round(len(sequence) ** 0.5)
    num_rows, reminder = divmod(len(sequence), num_columns)
    num_rows += bool(reminder)
    return [tuple(sequence[i::num_rows]) for i in range(num_rows)]

animals = 'drake fawn heron ibex koala lynx tahr xerus yak zapus'.split()
table = columnize(animals)
print(table) # [('drake', 'koala', 'yak'), ('fawn', 'lynx', 'zapus'), ('heron', 'tahr'), ('ibex', 'xerus')]
```

## Generic mappings

Use the syntax `MappingType[KeyType, ValueType]`. The `dict`, the mappings from `collections` and `collections.abc` support this notation since python 3.9.

```python
import sys
import re
import unicodedata
from collections.abc import Iterator

RE_WORD = re.compile(r'\w+')
STOP_CODE = sys.maxunicode + 1

def tokenize(text: str) -> Iterator[str]:
    """return iterable of uppercased words"""
    for match in RE_WORD.finditer(text):
        yield match.group().upper()
    
def name_index(start: int = 32, end: int = STOP_CODE) -> dict[str, set[str]]:
    index: dict[str, set[str]] = {}
    for char in (chr(i) for i in range(start, end)):
        if name := unicodedata.name(char, ''):
            for word in tokenize(name):
                index.setdefault(word, set()).add(char)
    return index
```

## Abstract classes

Ideally, a function should accept abstract types such as

```python
from collections.abc import
def name2hex(name: str, color_map: Mapping[str, int]) -> list[str]:
```

Using `abc.Mapping` allow the user to use a instance of `dict`, `defaultdict`, `ChainMap`, a subclass of `UserDict`. Notice that the return is a concrete type of `list[str]` because according with Postel's law (be conservative to what you send and liberal to what you receive)

The exception is the numbers that is preferable to use `int`, `float` or `complex` instead of `abc.Number`

## `abc.Iterable`

It's preferable to use `Iterable` and `Sequence` in the function's type hints.

```python
from collections.abc import Iterable

FromTo = tuple[str, str]

def zip_replace(text: str, changes: Iterable[FromTo]) -> str:
    for from_, to in changes:
        text = text.replace(from_, to)
    return text

l33t = [('a', '4'), ('e', '3'), ('i', '1'), ('o', '0')]
text = 'mad skilled noob powned leet'
zip_replace(text, l33t)
# 'm4d sk1ll3d n00b p0wn3d l33t'
```

The difference between a `abc.Sequence` and `abc.Iterable` is that in the first we are concerned about the size of the parameter, while in the second, in general we assume that we will perform the operation defined in the function for all members of the iterable.

## Parametrized generic and `TypeVar`

A generic type is parametrized when it's written like `list[T]` where `T` is a variable type that might be linked to a different type at every use. This allow that a input be reflect in the output of a function dynamically, but they are the same type.


```python
from collections.abc import Sequence
from random import shuffle
from typing import TypeVar

T = TypeVar('T')

def sample(population: Sequence[T], size: int) -> list[T]:
    if size < 1:
        raise ValueError('size must be >= 1')
    result = list(population)
    shuffle(result)
    return result[:size]
```

`TypeVar` is a hack to accomplish this idea. When used for the input it will mean any type, but in the output, it means the same type as the input.

A `TypeVar` might be restricted to certain types, like `NumberT = TypeVar('NumberT', float, Decimal, Fraction)`

Even more, we can delimit a limit to where a TypeVar might be extender with the `bound` keyarg in the TypeVar creation. For example, `HashableT = TypeVar('HashableT', bound=collection.abc.Hashable)`

Finally, we have the type `typing.AnyStr` that is a `TypeVar` defined as `AnyStr = TypeVar('AnyStr', bytes, str)` that can be used for methods that accept these both types.

## Protocols

Question: I did not get the idea from the book's definition

```python
from typing import Protocol, Any

class SupportLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...
```

A type `T` is consistent-with a protocol `P` if `T` implements all methods defined in `P`.

TODO: See this section again after reading the chapter 13.

TODO: finish the notes from here to the rest of the chapter after the meeting

## `Callable`

## `NoReturn`


# Only positional parameters

# Wrong typing errors

Since type hints are a new feature in python, we still can find problems of false positives (mypy will complain about correct code) and false negatives (mypy will not complain about incorrect code)
