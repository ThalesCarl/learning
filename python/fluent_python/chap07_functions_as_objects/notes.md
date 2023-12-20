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

