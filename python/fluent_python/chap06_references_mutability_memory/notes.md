# Variables are not boxes

A better way to describe them is as labels that links a name to an object.

```python
a = [1, 2, 3]
b = a # creates two labels to the same object, it does not copy
a.append(4)
print(b) # [1, 2, 3, 4]
```

The variable is always attributed to the object and not the object is attributed to the variable. The right side of a expression is always evaluted first and after the object is labeled with the name on the left side.

```python
class Gizmo():
    def __init__(self):
        print(f'Gizmo id: {id(self)}')

x = Gizmo() # Gizmo id: 4301489152 
y = Gizmo() * 10
# Gizmo id: 4301489432
# TypeError: unsupported operand type(s) for *: 'Gizmo' and 'int
print(y) # undefined y variable
```

Notice that when we do `y = Gizmo() * 10` the object is created, then it tries to multiply by 10, a exception is trown and the variable y is not associated with any object.

# Identity, equality and aliases

```python
charles = {'name': 'Charles L. Dogson', 'born': 1832}
lewis = charles
print(lewis is charles) # True
print(id(charles), id(lewis)) # (4300473992, 4300473992)
lewis['balance'] = 950
print(charles) # {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}

# but if we create another object with the same attributes
alex = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}
alex == charles # True, because all fields of the dict are equal
alex is not charles # True, because it is different objects
```

The identity, i. e., the function `id()` will never change for a python object. You can think of it as the object memory address. The operator `is` compares the `id()` of objects, while the operator `==` evaluates the `__eq__` function of a object to compare it to another. Our code would likely never call `id()` function directly because we use the `is` operator instead.

The most common use of `is` to compare with the `None` concept (which is a singleton, btw).

Other use is the comparisson with sentinel objects

```python
END_OF_DATA = object()
# ... many lines
def transverse():
    # ... more lines
    if node is END_OF_DATA:
        return
    # ... more stuff
```

The `is` operator is faster than the `==` because it can't be overloaded. While, the `a == b` is equivalent to `a.__eq__(b)` that can be just comparing the objects ids or something else more meaningfull. However, since we are more interested in the equallity of object and not the identity, we will most likely use the `==` operator.

## Tuples immutability

As we have seen before, a tuple is immutable, but if it is composed of mutable objects, then the tuple content can be changed because the immutability of a tuple is only relative to the references that it stores.

# Copies

```python
l1 = [3, [55, 44], (7, 8, 9)]
l2 = list(l1)
l2 == l1 # True
l2 is l1 # False

```
The use of `l[:]` creates a shallow copy
```python
# Shallow copy? I have tried modifying l3 but it did not changed l1
l3 = l1[:]
l3 == l1 # True
l3 is l1 # False
```

```python
l1 = [3, [66, 55,44], (7, 8, 9)]
l2 = list(l1)
l1.append(100)
l1[1].remove(55)
print('l1:', l1) # [3, [66, 44], (7, 8, 9), 100]
print('l2:', l2) # [3, [66, 44], (7, 8, 9)]

l2[1] += [33, 22]
l2[2] += (10, 11)
print('l1:', l1) # [3, [66, 44, 33, 22], (7, 8, 9), 100]
print('l2:', l2) # [3, [66, 44, 33, 22], (7, 8, 9, 10, 11)]

```

Notice that removing `55` from `l1` changed `l2` because we changed a mutable object inside of l1. When adding `+=` with a list, this changed both lists, but when adding `+=` with a tuple, a new tuple is created and placed on the l2 list.

## Deep and shallow copies

Use the builtin module  `copy` to create deep and shallow copies with the functions `deepcopy()` and `copy()` respectively.

```python
class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)
    
    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

import copy
bus1 =  Bus(['Alice', 'Bill', 'Claire', 'David'])
bus2 = copy.copy(bus1)
bus3 = copy.deepcopy(bus1)
id(bus1), id(bus2), id(bus3) # (4301498296, 4301499416, 4301499752)
bus1.drop('Bill')
bus2.passengers # ['Alice', 'Claire', 'David']
bus3.passengers # ['Alice', 'Bill', 'Claire', 'David']
id(bus1.passengers), id(bus2.passengers), id(bus3.passengers) # (4302658568, 4302658568, 4302657800)
```

Notice that `bus1` and `bus2` have the same reference to the list while `bus3` is a different passegers list

However, deepcopies might cause problems because the creation of them might cause a infinite loop because of cyclic references

```python
a = [10, 20]
b = [a, 30]
a.append(b)
print(a) # [10, 20, [[...], 30]]
c = deepcopy(a)
print(c) # [10, 20, [[...], 30]] # here the deepcopy function behaves as expected but it could cause problem XD
```

# Function parameters as references

The only way of passing a object to a function in Python is the **call by sharing**, which means the function can modify any mutable object that it receives but it cannot change its identity, i. e., it cannot sustitute a object by another one integrally.

```python
def f(a, b):
    a += b
    return a

x, y = 1, 2
f(x, y) # 3
print(x, y) # (1, 2) - Question: it did not changed x becuase x is a int and not reference?

a = [1, 2]
b = [3, 4]
f(x, y) # [1, 2, 3, 4]
print(a, b) # ([1, 2, 3, 4], [3, 4])

t = (10, 20)
u = (30, 40)
f(t, u) # (10, 20, 30, 40)
print(t, u) # ((10, 20), (30, 40))
```

## Mutable types as default 

This is a bad idea.
```python
class Bus:
    def __init__(self, passengers=[]):
        self.passengers = passengers
    
    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

bus1 = Bus(['Alice', 'Bill'])
bus1.passengers # ['Alice', 'Bill']
bus1.pick('Charlie')
bus1.drop('Alice')
bus1.passengers # ['Bill', 'Charlie']

bus2 = Bus()
bus2.pick('Carrie')
bus2.passengers # ['Carrie']

bus3 = Bus()
bus3.passengers # ['Carrie'] # Here is the problem, the default list was changed by the bus2.pick() function

bus3.pick('Dave')
bus2.passegers # ['Carrie', 'Dave'] # Again the same list is used

bus2.passengers is bus3.passengers # True
bus1.passengers # ['Bill', 'Charlie']
```

## Defensive programming with mutable arguments

```python
class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers
    
    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
bus = TwilightBus(basketball_team)
bus.drop('Tina')
bus.drop('Pat')
basketball_team # ['Sue', 'Maya', 'Diana'] - Notice that the bus object changed the basketball_team list
```

The problem is that `self.passengers = passengers` is labeling the `self.passengers` to the list `passengers` passed on the constructor. The correct way is to create a copy of the list in the initialization of the function with `self.passengers = list(passengers)`. As a bonus, the call to the `list()` method let the constructor of `Bus` receive any iterable. Even more, because we are creating our new list, we unsure that we would have the methods `append()` and `remove()` necessary.

# The `del` command and garbage collection

The `del` command erases references and not objects, which means in the code below that even tough `a` and `b` are pointing to the same object, when we delete `a`, the `b` reference is still good. When we associate `b`  to a new object, then the garbage collector will be able to remove the previous one.
```python
a = [1, 2]
b = a
del a
print(b) # [1, 2]
b = [3]
```

Notice that we call `del a` because `del` is command and not a function `del(a)`, even though the later is valid as well.

There is a `__del__` function that might be implemented to control the deletion of an object, but it is really rare the cases where we may want to implement it.

# Traps of immutable objects in python

For a tuple `t`, the call `t[:]` does not create a copy of the tuple, but returns a reference to the same object, just like `tuple(t)`. This is observed in `str`, `bytes`, and `frozensets` as well. This is the opposite of what a call to `list()` of `l[:]` do.

```python
# tuples
t1 = (1, 2, 3)
t2 = tuple(t1)
t2 is t1 # True
t3 = t1[:]
t3 is t1 # True

t4 = (1, 2, 3)
t4 is t1 # False

s1 = 'ABC'
s2 = str(s1)
s2 is s1 # True
s3 = 'ABC'
s3 is s1 # True. Surprise, mf. This is due to the string literal sharing made by the python interpreter.
```