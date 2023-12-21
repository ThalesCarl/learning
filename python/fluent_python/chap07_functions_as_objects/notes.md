# First order objects

A object of first order is an entity that may be:
- Created during the execution of a program
- Set to a variable or a element in a data structure
- Passed as an argument to a function
- Returned as a result of a function

Examples of first order objects are int, string and dict. But surprise, in python functions are also first order objects, which is essential to functional languages, such as Haskell, Elixir or Clojure.

```python
def factorial(n):
    """returns n!"""
    return 1 if n < 2 else n * factorial(n -1)

factorial(6) # 720
factorial.__doc__ # 'returns n!'
type(factorial) # <class 'function'>
# Notice that `factorial` is an object of the `function` class, which means

fact = factorial # we can attribute to another variable
map(fact, range(6)) # and we can pass it as an argument to another function
# output: [1, 1, 2, 6, 24, 120]
```

# High order functions

A function that receives a function as argument or returns a function as result is a high order function. Example: `sorted` in which the `key=` argument is used to indicate how the list is sorted

```python
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
# Sort fruits by the length
sorted(fruits, key=len)
['fig', 'apple', 'cherry', 'banana', 'raspberry', 'strawberry']

# Sort fruits by its reversed order (to find rhymes)
def reverse(word):
    return word[::-1]
reverse('testing') # 'gnitset'
sorted(fruits, key=reverse)
['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']
```

On functional programming, the most known high order functions are `map`, `filter`, `reduce` and `apply`. The first three are available on Python 3, but `apply` was removed. Instead of using `apply(fn, args, kwargs)`, use directly `fn(*args, **kwargs)`.

Since the introduction of list comprehensions, `map` and `filter` are less used, because they are less legible than list comps.

```python
list(map(factorial, range(6)))
[factorial(n) for n in range(6)]

list(map(factorial, filter(lambda n: n % 2, range(6))))
[factorial(n) for n in range(6) if n % 2]
```

Notice that `filter` and `map` are builtin and `reduce` is part of `functools` module. The most common usage of `reduce` that was summing items using the `operator.add` was replaced by the builtin function `sum`. Other builtin functions that could replace `reduce` function are:

- `all(iterable)` returns `True` if there is no false element is the iterable;
- `any(iterable)` returns `True` if any element of the iterable is `True`

# Anonymous functions (`lambda` functions)

Use the keyword `lambda` to create a function that has no name.

Notice that a lambda function cannot have non pure expressions, which includes the `while`, `for` or `try` concepts. You cannot use the `=` attribution sign in a lambda function, unless you use the walrus operator (`:=`). But beware, using this operator usually means that you would be better defining a regular function.

```python
# using the lambda to replace the reverse function defined before
sorted(fruits, key=lambda word: word[::-1])
```

A lambda function is just syntax sugar to a regular function defined with a `def`, which means there's no performance difference between them

# Nine flavors of invocable objects

The `()` invocation operator can be applied to other objects besides functions. To see if an object can be invocable, use the `callable()` builtin function.

The following objects are invocable (in python 3.9):

- Functions defined by the user: using `def` or `lambda` keywords
- Builtin functions. Implemented in C when we are using CPython (most common). Example: `len`
- Builtin methods: Methods (of builtin objects?) implemented in C. Example: `dict.get`.
- Methods: functions defined in the scope of a class
- Classes: when invocated a class will call its `__new__` and `__init__` method in sequence, to create and initialize a instance. Then, the instance is returned to the user. 
- Class instance (objects): execute the `__call__` function of a class if it is defined, otherwise raise an `TypeError: object is not callable` exception.
- Generator functions: functions or methods that use the `yield` in this body. When invocated, they return an generator object
- Native coroutines functions: functions or methods defined using the `async def` keywords. When invocated, returns an coroutine object. Introduced in Python 3.5
- Asynchronous generator functions: functions or methods defined using the `async def` that have a `yield` in its body. When invocated, returns a asynchronous generator that might be used in an `async for`. Introduced in Python 3.6

The last three will be seen in chapter 17 and 21.

# User defined invocable types

Not only functions are objects, but you can make objects behave like functions in python. To do so, you just need to implement the `__call__` instance method.

```python
import random

class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self.items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        return self.pick()

bingo = BingoCage(range(3)) # _items: [2, 0, 1]
bingo.pick() # 1, _items: [2, 0]
bingo() # 0, _items: [2]
callable(bingo) # True
```

# Named and positional arguments for a function

Positional parameters are the specified using the position they are in the function call. Example: `f('foo', 'baa')` takes two positional parameters
Named parameters are the specified using `f(bar='foo')`

```python
def tag(name, *content, class_=None, **attrs):
    """Generate one or more HTML tags"""
    if class_ is not None:
        attrs['class'] = class_
    attrs_pairs = (f' {attr} = "{value}"' for attr, value
                        in sorted(attrs.items()))
    attr_str = ''.join(attrs_pairs)
    if content:
        elements = (f'<{name}{attr_str}>{c}</{name}'
                    for c in content)
        return '\n'.join(elements)
    else:
        return f'<{name}{attr_str} />'

tag('br') # '<br />' - it just hit the last else
tag('p', 'hello') # '<p>hello</p> - hello is captured by *content as a tuple, just like any other positional arguments
tag('p', 'hello', 'world')
# '<p>hello</p>'
# '<p>world</p>'
tag('p', 'hello', id=33) # '<p id="33">hello</p>' - any named arg that is not mentioned in the **attrs as an dict
tag('p', 'hello', 'world', class_='sidebar')
# '<p class="sidebar">hello</p>'
# '<p class="sidebar">world</p>'
tag(content='testing', name='img')
# '<img content="testing" /> - you can pass the first positional argument as a named parameter as well
my_tag = {
    'name': 'img',
    'title': 'Sunset Boulevard',
    'src': 'sunset.jpg',
    'class': 'framed',
}
tag(**my_tag) # You can pass all the named arguments as a dict using **
# '<img class="framed" src="sunset.jpg" title="Sunset Boulevard" />' 
# Notice that the 'class' is a valid name because it does not collide with class_
# and with the keyword class, because it is a string
```

In order to specify only named parameters, the previous parameter must have a `*`. If you don't want to include positional arguments, place a `*` alone in the function signature.

```python
# Takes one positional argument 'a' and one named argument 'b'
def f(a, *, b):
    return a, b

f(1, b=2) # (1, 2)
f(1, 2) # TypeError: f() takes 1 positional argument but 2 were given
f(1) # TypeError: f() missing 1 required keyword-only argument: 'b'
f(1, b=2, c=3) # TypeError: f() got an unexpected keyword argument 'c'
```

## How to make a parameter only positional

Since Python 3.8, using the `/` after a parameter makes it only positional. 

```python
# This function can only be called divmod(1, 2) and not divmod(a=1, b=2)
def divmod2(a, b, /):
    return (a // b, a % b)
```

# Functional programming packages

Even if python is not project to be a functional programming language, there are some packages that may help you to use Python as such.

# `operator` module

The operator is useful when you want to use the `reduce()` function but does not want to define your own `lambda` functions. For example, suppose you want to implement a factorial without the recursion, you could use `reduce()` with or without the `lambda` definition as below:

```python
from functools import reduce

def factorial(n):
    return reduce(lambda a, b: a*b, range(1, n+1))

from operator import mul
def factorial(n):
    return reduce(mul, range(1, n+1))
```

`itemgetter` is used to extract items of sequences or read object attributes

```python
metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

from operator import itemgetter
for city in sorted(metro_data, key=itemgetter(1)):
    print(city)
# The cities ordered by the country id
# ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833))
# ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889))
# ('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
# ('Mexico City', 'MX', 20.142, (19.433333, -99.133333))
# ('New York-Newark', 'US', 20.104, (40.808611, -74.020386))
# It could be also:
for city in sorted(metro_data, key=lambda: fields: fields[1]):
```


You can pass more than an argument to `itemgetter`, this will return a function that will return a tuple with the items specified.

`attrgetter` is used to extract attributes by name

```python
from collections import namedtuple
LatLon = namedtuple('LatLon', 'lat lon')
Metropolis = namedtuple('Metropolis', 'name cc pop coord')
metro_areas = [Metropolis(name, cc, pop, LatLon(lat, lon))
                for name, cc, pop, (lat, lon) in metro_data]
metro_areas[0]
# Metropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLon(lat=35.689722, lon=139.691667))
metro_areas[0].coord.lat  # 35.689722
from operator import attrgetter
name_lat = attrgetter('name', 'coord.lat')
for city in sorted(metro_areas, key=attrgetter('coord.lat')):
    print(name_lat(city))
```

`methodcaller` invokes a method of an object passed as argument

```python
from operator import methodcaller
s = 'The time has come'
upcase = methodcaller('upper')
upcase(s) # 'THE TIME HAS COME' - equivalent to s.upper()

hyphenate = methodcaller('replace', ' ', '-')
hyphenate(s) # 'The-time-has-come' - Maybe more clear than '-'.join(s) but more verbose
```

## `functools.partial`

This guy lets you create a function from another, fixing one or more positional arguments.

```python
from operator import mul
from functools import partial
triple = partial(mu, 3) # Create a new function from mul, but linking the first positional argument to 3
triple(7) # 21
list(map(triple, range(1, 10)))
# [3, 6, 9, 12, 15, 18, 21, 24, 27]

# Useful usage
import unicodedata, functools
nfc = functools.partial(unicodedata.normalize, 'NFC')
nfc('café') # instead of normalize('NFC', 'café')

# Usage with tag() function defined before
picture = partial(tag, 'img', class_='pic-frame')
picture(src='umps.jpg') # <img class="pic-frame" src="wumpus.jpeg" />'
```