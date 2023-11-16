# Built in sequencies

- Containers: Can hold different types of data, including inner containers. Examples: list, tuple and collection.deque
- Plain sequencies: store simple objects. Examples: str, bytes, array.array.

Containers hold just references to the objects it contains, while plain sequencies holds its contents in the memory addres.

Every python object has a header with metadata.

# Sequencies according with mutability

- Mutable sequencies: list, bytearray, array.array and collections.deque
- Imutable sequencies: tuple, str and bytes.

# List comprensions and generator expressions

A listcomp is always a method of creating a new list. 

It should be concise. If it exceeds two lines, it should be written as an old for loop. 

Variable created inside a listcomp are not acessible outside its scope, except for the ones created using the walrus operator (`:=`)

```python
x = 'ABC'
codes = [last := ord(c) for c in x]
print(last) # available
print(c) # not available
```

Listcomps do everything a map/filter do, but without the extra steps.

```python
symbols = '$¢£¥€¤'
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
```

Listcomps can be used more than once to create a cartesian product.

```python
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for color in colors for size in sizes]
print(tshits)
# [('black', 'S'), ('black', 'M'), ('black', 'L'), ('white', 'S'),
# ('white', 'M'), ('white', 'L')]
```

On the other hand, genexpr are ways to create other types but lists, just like a listcomp.

```python
symbols = '$¢£¥€¤'
tuple(ord(symbol) for symbol in symbols) # notice the need to use tuple keyword to transform a genexp into a tuple
array.array('I', (ord(symbol) for symbol in symbols)) # works fine

# but why does making the following doesnot work
a = (ord(symbol) for symbol in symbols)
array.array('I', a)
```

Generator expressions are useful when you dont need to keep the value in the memory. For example:

```python
for tshirt in (f'{c}{s}' for c in colors for s in sizes):
    print(tshirt)
```

# Tuples are not just immutable lists

Besides being a immutable list, tuples can be used as unnamed registers.

Unnamed registers are variables where the position indicates the meaning of the data.

```python
lax_coordinates = (33.9425, -118.408056)
city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014)
travelers_ids = [('USA','31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
for passport in sorted(travelers_ids):
    print('%s/%s' % passport) # it gets that every #s is for one member of the tuple

for country, _ in travelers_id: # tuple are useful for unpacking
    print(country)
```

A tuple is immutable list, but the items that a tuple contains could be mutable. This can led to a miriad of bugs. For example, a tuple that contain a mutable object cannot be used as key in a dict or a element in a set.

The dunder methods available for tuples are the same as for lists, except the ones that evolves addition or removal of components and the `__reversed__`.

# Unpacking

Unpacking avoids the use of indexes to break a sequence, which is unnecessary and error prune.

Any object can be unpacked, including iterators that dont support the index notation `[]`.

The only requirement is the iterator must produce one item per variable, except when we are using the `*` operator.

Parallel unpacking: break a sequence into items. Example `latitude, longitude = (33.9425, -118.48056)`

Other unpacking example is

```python
t = (20, 8)
result = divmod(*t) # using the *t is unpacking because the function divmod receives two number and not a tuple
quotient, remainder = result # this is a unpacking example as well
```

You can also use the `*` operator to get the rest of a iterator into a variable

```python
a, b, *rest = range(5) # a = 0, b = 1, rest = [2, 3, 4]
a, b, *rest = range(3) # a = 0, b = 1, rest = [2]
a, b, *rest = range(2) # a = 0, b = 1, rest = []
a, *rest, c, d = range(5) # a = 0, rest = [1, 2], c = 3, d = 4
*rest, b, c, d = range(5) # rest = [0, 1], b = 2, c = 3, d = 4
```

Using the `*` operator in funcion definitions:

```python
def fun(a, b, c, d, *rest): # did not get what does it mean to have * in the function definition
    return a, b, c, d, rest

fun(*[1, 2], 3, *range(4, 7)) # (1, 2, 3, 4, (5, 6))
```

Unpacking aligned tuples: see example `nested_sequences.py`

You can also use a list or a tuple as the target of the unpacking, but beware that this is rare. However, remember that tuples with one item must have a trailing comma: `(record, ) = my_function()`. If you forget this comma, you are causing a silent bug.

# Pattern matching

Available for python 3.10 and forward.

Example: imagine you are building a robot that receives a message

```python
def hangle_command(self, message):
    match message:
        case ['BEEPER', frequency, times]: # match any 3 items sequence if the first element is 'BEEPER'
            self.beep(times, frequency)
        case ['NECK', angle]: # match any 2 items sequence if the first element is 'NECK'
            self.rotate_neck(angle)
        case ['LED', ident, intensity]:
            self.leds[ident].set_brightness(ident, intensity) # match any 3 items sequence if the the first element is 'LED'
        case ['LED', ident, red, green, blue]:
            self.leds[ident].set_color(ident, red, green, blue) # match any 5 items sequence if the first element is 'LED'
        case _: # default case, what happens if none of the previous case was met
            raise InvalidCommand(message)
```

See `nested_sequences.py` on how to use pattern matching for solving the same problem. You can use lists or tuples as the pattern, but they dont make a lot of difference.

In the pattern matching context, `str`, `bytes` and `bytearray` are not treated as sequences, because these types are used as their atomic value. This means a `str` will match with other `str` but not with individual chars. Question: am I right?

The `_` is a placeholder for any value that doesnt match with the pattern. This value is discarded. Also `_` is the only variable that can be repeated in a pattern matching expression.

You can link any part of a pattern to a variable using the keyword `as`

```python
record = ['Shanghai', 'CN', 24.9, (31.1, 121.3)]
match record:
    case [name, _, _, (lat, lon) as coord]
        print(name) # Shanghai
        print(coord) # (31.1, 121.3)
```

We can make the patterns more specific using the types expected in the `case` definition. For example change `case [name, _, _, (lat, lon)]` to `case [str(name), _, _, (float(lat), float(lon))]`. Notice that even tought, it seems that we are making a cast to another type with this definition, we are in fact just telling the type to the pattern matching expression.

To match any number of arguments that can be discarded, use `*_`. For example: `case [name, *_, (lat, lon)]`

The optional guard `if`  is only evaluated if the pattern match, and it is possible to use the variables defined in the pattern

TODO: review with the guys the `lis.py` example of section 2.6.1

# Slicing

Slices always exclude the last item, because of the C convention of starting a array at index 0

```python
l = [10, 20, 30, 40, 50, 60]
l[:2] # [10, 20]
l[2:] # [30, 40, 50, 60]
l[1:5] # [20, 30, 40, 50]
l[1:5:2] # [20, 40]
s = 'bicycle'
s[::3] # 'bye'
s[::-1] # 'elcycib', invert order using slicing
s[::-2] # 'eccb'
```

The notation `a:b:c` is only valid betwenn `[]` and produces a slice object: `slice(a, b, c)`, that can be useful when you want to split a line in a known range.

The dunder methods `__getitem__` and `__setitem__` will use the arguments passed to `[]` with commas as a tuple input. This is used in numpy to get something like `m[m:n, k:l]`, but it is not acceptable in Python lists.

Except for `memoryview`, all builtins Python objects are unidimentional and don't accept the `a[1, 2]` notation. 

The ellipsis (`...`) can be used by some places in numpy, but not in the standard python lib.

Slices can be used to do inplace attribution:

```python
l = list(range(10)) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
l[2:5] = [20, 30] # [0, 1, 20, 30, 5, 6, 7, 8, 9]
del l[5:7] # [0, 1, 20, 30, 5, 8, 9]
l[3::2] # [0, 1, 20, 11, 5, 22, 9]
l[2:5] = 100 # Error: can only assign an iterable
l[2:5] = [100] # [0, 1, 100, 22, 9]
```

# Using `+` and `*` with sequences

To use this operators, the sequences must be of the same type and a new sequence will be created from this same type.

```python
l = [1, 2, 3]
l * 5 # [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
5 * 'abcd' # 'abcdabcdabcdabcdabcd'
```

But beware, lists of lists are not suppose to be started with the notation `[[]] * n` because this will create a list of the same list, i. e., when you try to modify on item of one of the internal list, it will modify all of them.

# Using `+=` and `*=` with sequences

The dunder method that do `+=` work is `__iadd__`, which stands for in-place addition, but if `__iadd__` is not implemented, python will call `__add__`. For lists, bytearrays and array.array, `a += b` is equal to `a.extend(b)`, for other object it will do `a = a + b`, where first `a + b` is computed and stored in a new object that will be afterwards emplaced above previous value of `a`.

The same ideas are valid for `*=` which used the `__imut__` method.

```python
l = [1, 2, 3]
l *= 2 # [1, 2, 3, 1, 2, 3] same memory addres
t = (1, 2, 3)
t *= 2 # (1, 2, 3, 1, 2, 3) different memory address because tuples are immutable, hence a new object was created
```

Avoid putting mutable objects in tuples just to prevent the error below

```python
t = (1 , 2, [30, 40])
t[2] += [50, 60] # Produces a exception but modifies the object anyway
t # (1, 2, [30, 40, 50, 60])
```

# Sorting

There are two sorting methods in python: the buildin `sorted()` function and the `list.sort()` method. The differnce is that the `list.sort()` will perform the sorting in place and will return a `None` to explicity say that. On the other hand, `sorted()` will get any iterable, sort it and return a new object.

Both methods have two optional parameters:
  - `reverse`: if true, the order is decrescent.
  - `key`: a function that will be used to compare the elements of the iterable.

```python
fruits = ['grape', 'raspberry', 'apple', 'banana']
sorted(fruits) # ['apple', 'banana', 'grape', 'raspberry'] # alfabetic order
sorted(fruits, reverse=True) # ['raspberry', 'grape', 'banana', 'apple']
sorted(fruits, key=len) # ['grape', 'apple', 'banana', 'raspberry'] 
fruits.sort() # ['apple', 'banana', 'grape', 'raspberry'] # change the original list
```

After a list is ordered you can search in it using the builtin method `bisect`. You can also add a item to a sorted list using the `bisect.insort(seq, item)` to keep the list in order

# Other sequences

## Arrays

An `array.array` is ideal for substitute a list composed of only floating point numbers. This data structure is really close to a C array. You will pass in the construction the type of the array using the `typecode`, which is a letter. For example, `b` indicates that the array will have only items that have one byte.

```python
from array import array
from random import random
floats = array('d', (random() for i in range(10**7)))
```

Arrays are way faster than lists, around 60 times faster.

For specific binary data, python has `bytes` and `bytearray` that will be discussed in chapter 4.

Also arrays have the following interesting funcions:
  - s.frombytes(b): read from a `bytes` object `b`
  - s.fromfile(f, n): read `n` items from `n` file
  - s.fromlist(l): add items from a list `l`. If one raises a `TypeError`, no item is added.

Until Python 3.10, an `array` does not have the `a.sort()` function. If you need to sort an array, you need to use the `sorted()` builtin function.

## Memoryviews

The builtin `memoryview` object is similar to an `np.array` without the math support. It allows to share memory between arrays without the need to copy bytes. Use the `.cast()` to create a new memoryview from a previous one sharing the same memory.

```python
from array import array
octets = array('B', range(6))
m1 = memoryview(octets)
m1.tolist() # [0, 1, 2, 3, 4, 5]
m2 = m1.cast('B', [2, 3])
m2.tolist() # [[0, 1, 2],[3, 4, 5]]
m3 = m1.cast('B', [3, 2])
m3.tolist() # [[0, 1], [2, 3], [4, 5]]
m2[1, 1] = 22
m3[1, 1] = 33
print(octets) # [0, 1, 2, 33, 22, 5]

# Bad usage
numbers = array('h', [-2, -1, 0, 1, 2])
memv = memoryview(numbers)
len(memv) # 5
memv[0] # -2
memv_oct = memv.cast('B')
memv_oct.tolist() # [254, 255, 255, 255, 0, 0, 1, 0, 2, 0]
memv_oct[5] = 4
numbers # [-2, -1, 1024, 1, 2] 
```

## Numpy arrays

This lib implements multidimensional arrays and matrices.

It is base of `scipy` which implements a lot of algorithms of linear algebra, numeric calculus and statistics.

```python
import numpy as np
a = np.arange(12)
a.shape # (12,)
a.shape = 3, 4 # create a matrix
```

## Deques

A list can be used as an `stack` with the `.append` and `.pop` methods, and as a `queue` with the `.append` and `.pop(0)` methods. but the `.pop(0)` is expensive because it needs to realocate all the items of the list. Here it comes the `collections.deque` data structure, that is a double ended queue that is designed to be fast in the insertion and deletion processes.

```python
from collections import deque
dq = deque(range(10), maxlen=10)
dq.rotate(3) # Take 3 items from the right and insert them on the left
print(dq) # [7, 8, 9, 0, 1, 2, 3, 4, 5, 6]
dq.rotate(-4) # Take 4 items from the left and insert them on the right
print(dq) # [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
dq.appendleft(-1) # Adding items to a full deck will descard the last one
print(dq) # [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
dq.extend([11, 22, 33])
print(dq) # [3, 4, 5, 6, 7, 8, 9, 11, 22, 33]
dq.extendleft([10, 20, 30, 40])
print(dq) # [40, 30, 20, 10, 3, 4, 5, 6, 7, 8]
```

A `deque` will implement most of the list's methods and some specific ones.

Notice that removing items from the middle is expensive. Question: inserting is not? Why?

The operations `append` and `popleft` are atomic, hence, they can be used safely in a multithread application without locks.

## Other types

- `queue` implements `SimpleQueue`, `Queue`, `LifoQueue` and `PriorityQueue`
- `multiprocessing` implements `SimpleQueue` and `Queue` used to communication between processes.
- `asyncio` implements `Queue`, `LifoQueue`, `PriorityQueue` and `JoinableQueue` used for asyncronous programming.
- `heapq` allows to use a queue of heap type (What does this mean?)