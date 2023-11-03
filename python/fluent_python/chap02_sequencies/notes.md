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

## Tuples are not just immutable

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