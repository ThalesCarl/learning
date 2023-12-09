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