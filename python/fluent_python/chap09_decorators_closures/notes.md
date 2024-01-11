# Decorators introduction

A decorator is a callable that receives another function as an argument, the decorated function.

The decorator can execute some processing with the decorated function, and/or return it or substitute it or even return an invocable object.

```python
@decorate
def target():
    print('running target')

# The code above is the same as
def target():
    print('running target')

target = decorate(target)
```

In general, the decorator will return a function different than the function that was passed to it.

```python
def deco(func):
    def inner():
        print('running inner')
    return inner

@deco
def target():
    print('running target')

target() # Out: running inner
```

Notice that the `'running target'` is not printed to the console in the definition above. In order to make it show, we need to add a `func()` call inside the `inner()` definition. If we add a `func()` call to the `deco()` definition, before the `return` statement, the string will be printed when we are defining the function with the decorator.

Always remember:
* A decorator is a function or another callable
* A decorator can replace the decorated function by another function
* Decorators are executed immediately when a module is loaded

# When a decorator is called

The decorator is executed after the function is defined. This happens in the importation time (when a module is loaded by the python interpreter)

```python
registry = []

def register(func):
    print(f'running register({func})')
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')

@register
def f2():
    print('running f2()')

def f3():
    print('running f3()')
    
def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()

if __name__ == '__main__':
    main()
```

If we execute the code above as a script, the output would be

```text
$ python3 registration.py
running register(<function f1 at 0x100631bf8>)
running register(<function f2 at 0x100631c80>)
running main()
registry -> [<function f1 at 0x100631bf8>, <function f2 at 0x100631c80>]
running f1()
running f2()
running f3()
```

If we import the code above as module, the output would be:

```text
>>> import registration
running register(<function f1 at 0x10063b1e0>)
running register(<function f2 at 0x10063b268>)
```

# Variable scope (a recap)

```python
def f1(a):
    print(a)
    print(b)

f1(3) # Error: b is not defined

b = 6 # global variable
f1(3) # 6, 9


b = 6
def f2(a):
    print(a)
    print(b)
    b = 9

f2(3) # 3 and then Error: local variable 'b' referenced before assignment
```

Because of the `b = 9` line, python will assume that `b` is a local variable in the `f2()` definition. If we want that the interpreter uses `b` as a global variable in the function definition and attribute a different value to `b`, we need to use the `global` keyword, as follows

```python
b = 6
def f3(a):
    global b
    print(a)
    print(b)
    b = 9
f3(3) # 3, 6
print(b) # 9
```

Notice there's two scopes in action here:
* The global scope: names defined outside any function or class definition
* Local scope of a function: names passed as parameter or names defined inside the function definition

# Closure definition

In the python's context a closure is a function that is defined within other function and that uses the variables that are to this outer function (am I right?). Question: is it still a closure if a function is not returned?

See a example of calculating a historic average

```python
def make_averager():
    series = [] # free variable

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)
    return averager

avg = make_averager()
avg(10) # 10
avg(11) # 10.5
avg(15) # 12.0
```

Notice that the `series` argument is preserved in the function's object in the `avg.__code__.co_freevars` and its content is saved at `avg.__closure__[0].cell_contents`. 

A closure can also be seen a function that keeps the links to free variables that exist when a function is defined and that might be used later, even if the scope where the function definition is no longer available.

# The `nonlocal` keyword

If we try to use a immutable variable inside a closure, such as below we would run into the same problem seen in the variables scopes problem. In order to avoid this, we use the `nonlocal` keyword that acts like the `global` keyword but for variables defined in function that are defined inside other functions.

```python
def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    return averager
```

# A simple decorator implementation

The code below implements a decorator that count the time of the decorated function invocation


```python
import time

def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print(f'[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}')
        return result
    return clocked

@clock
def snooze(seconds):
    time.sleep(seconds)

snooze(0.123) # [0.12363791s] snooze(0.123) -> None
```

Notice that the decorator will replace the `snooze` function by the `clocked` function, then will execute the original function in the line `result = func(*args)`. That's the general idea of a decorator: replace the function by another that executes the original function and do some extra processing.

The above code could be improved to support named arguments and to avoid covering the `__name__` and `__doc__` arguments of the decorated function using the `@functools.wraps(func)` decorator (is this the metaverse?)

```python
import time
import functools

def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_lst = [repr(arg) for arg in args]
        arg_lst.extend(f'{k}={v!r}' for k, v in kwargs.items())
        arg_str = ', '.join(arg_lst)
        print(f'[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}')
        return result
    return clocked
```

# Standard lib's decorators

Python has three builtin decorators: `property`, `classmethod` and `staticmethod` that will be seen later in this book. Other useful decorators can be seen in the `functools` lib

## `functools.cache`

This decorator implements **memoization**, which is way to save previous results of a function.


```python
import functools

# import clock (previous example)

@functools.cache
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)

if __name__ == '__main__':
    print(fibonacci(6))
```

This way, the function is only called once for every number from 0 to 6, which is not the case if we didn't use the `@cache` decorator.

Important: all arguments that are taken by the function must be hashable, because the decorator uses a dict to store the results, in which, the keys are the positional arguments.

The most interesting usage of `@cache` is in functions that calls external APIs.

Beware: the `@cache` can consume a lot of memory if the items in the cache are too big.

## `functools.lru_cache`

This is the previous way of using the `@cache` decorator for python 3.8 and before. However, you can still use it in more modern python, because it has a more flexible signature.

The biggest advantage of `lru_cache` is the `maxsize` argument, which is used to limit the number of simultaneous entries.

LRU stands for **Least Recently Used**. This means that values that are not used for a while are discarded.


```python
# There are two ways of using it. 

# The first is
@lru_cache
def costly_function(a, b):
    
# The second (since python 3.2) is like a function, that accepts the following arguments:
# maxsize=128 (default). Number of max simultaneous entries. If None, it works like the @cache decorator. Important: always use base 2 number here for performance.
# typed=False. Whether to make different entries for arguments that might be considered equal, such as 1 and 1.0
@lru_cache(maxsize=2**20, typed=True)
def costly_function(a, b):
```


## `functools.singledispatch`

This decorator is a way of kind using function overloading (which is not available in python). The overloading only applies to the first positional argument. That's the reason why it's single and not multiple.
Imagine generating HTML content from different Python types 

```python
from functools import singledispatch
from collections import abc
import fractions
import decimal
import numbers
import html

@singledispatch
def htmlize(obj: object) -> str:
    content = html.escape(repr(obj))
    return f'<pre>{content}</pre>'

@htmlize.register
def _(text: str) -> str:
    content = html.escape(text).replace('\n', '<br/>\n')
    return f'<p>{content}</p>'

@htmlize.register
def _(seq: abc.Sequence) -> str:
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'

# To see more examples see the book
```

Question: how does this worked before type hints?

Hint: use always `abc`, `typing.Protocol`, `numbers` instead of `list`, `int` or `float` is better, because broader types might be included in your singledispatch call.

You can add the `htmlize.register` anywhere, not just close to the `htmlize()` default implementation.

# Parametrized decorators

A parametrized decorator is a decorator that receives arguments. To define one, we need to create a factory of decorators, that receives the arguments and returns a decorator, which is then applied to the function.

First recall this normal decorator implementation
```python
registry = = []

def registry(func):
    print(f'running register({func})')
    registry.append(func)
    return func

@register
def f1():
    print(f'running f1()')

print('running main()')
print('registry -> ', registry)
f1()
```


Now let's create a factory of decorators. The argument `active` is the parametrization and will indicate whether a function should be include in the registry.

```python
registry = set()

def register(active=True):
    def decorate(func):
        print('running register'
              f'(active={active})->decorate({func})')
        if active:
            registry.add(func)
        else:
            registry.discard(func) # Why?
        return func
    return decorate

@register(active=False)
def f1():
    print(f'running f1()')

@register()
def f2():
    print(f'running f2()')

def f3():
    print(f'running f3()')
```

Another example we can do is improve the `@clock` decorator, where the user will now be able to pass a format string to the decorator.

```python
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*_args):
            t0 = time.perf_counter()
            _result = func(*_args)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorate

if __name__ == '__main__':

    @clock('{name}: {elapsed}s')
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)

    

```