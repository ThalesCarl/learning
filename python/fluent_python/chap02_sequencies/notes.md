# Sequencies

## Built in sequencies

- Containers: Can hold different types of data, including inner containers. Examples: list, tuple and collection.deque
- Plain sequencies: store simple objects. Examples: str, bytes, array.array.

Containers hold just references to the objects it contains, while plain sequencies holds its contents in the memory addres.

Every python object has a header with metadata.

## Sequencies according with mutability

- Mutable sequencies: list, bytearray, array.array and collections.deque
- Imutable sequencies: tuple, str and bytes.

## List comprensions and generator expressions

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

## Tuples are not just immutable lists

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

## Unpacking

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

## Pattern matching

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