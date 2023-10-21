# Python's data model

Python data model is a interface to how you can iteract with the basics of the language. The interface is composed by methods that have a special syntax, which a double `__` before and after the method's name.

You should implement this special methods when you want to iteract with the following:
- Collections;
- Attributs access;
- Iteractions;
- Overloading of operators
- Methods and functions calls
- String representation and formating
- Asyncronous programming with `await` keyword;
- Objects's creation and destruction
- Managed contexts using the `with` and `async with` keywords.

## Pythonic Deck's

See file `pythonic_deck.py`. With that implementation of a `FrechDeck` we can easily use the `len()` and `random.choice` standard functions without any further implementation. Moreover, because we implemented `__getitem__()` we can use the default `[]` operator.

Question: how does `deck[12::13]` returns all the aces?

Furthermore, our `FrenchDeck` is iterable, then we can use

```python
for card in deck:
    print(card)

for card in reversed(deck):
    print(card)
```

Even more, we have available the keyword `in` because `FrenchDeck` is iterable:

```python
Card('Q', 'hearts') in deck # True
Card('7', 'beasts') in deck # False
```

In conclusion, when we implement `__len__` and `__getitem__` the `FrechDeck` class behaves just like a python standard sequence. 

## When to call for a special method

In general, you don't call the dunder method. You should call the builtin function that uses the dunder method, for example `len(x)` with call `x.__len__()`. The buildin funtion is faster and more pythonic. The only exception is the dunder method `__init__()` that you use to instantiate the base class of a class you are implementing the inheretance.

