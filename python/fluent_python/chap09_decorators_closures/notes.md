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