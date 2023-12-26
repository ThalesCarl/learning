This chapter is about using type hints for functions. For instance, the function below receives a `str` an return a list of `str`.

```python
def tokenize(s: str) -> list[str]:
    return s.replace('(', ' ( ').replace(')', ' ) ').split()
```

# Gradual type checking

Python type system is gradual, which means:
- It's optional: the type verifier doesn't say anything if a type is not provided by default. It assumes `Any` if cannot identify which type a object is.
- Do not capture typing errors during runtime
- Do not improve performance: even thought type hints provide information that might be used for optimization, for now they are not used yet.

See a usage example in the `type_hints_practice.py` file.

# Types classification

- Nominal typing: Objects and variables have types, but objects only exists during execution. Because of this, a type error might arise from the code static analysis.
- Duck typing: objects have types, but variables (including parameters don't). This means that a object type does not matter, as long as the operations that the object need are supported.

```python
class Bird:
    pass

class Duck(Bird):
    def quack(self):
        print('Quack!')

def alert(birdie):
    birdie.quack()

def alert_duck(birdie: Duck) -> None:
    birdie.quack()

def alert_bird(birdie: Bird) -> None:
    birdie.quack()

daffy = Duck()
alert(daffy)       # No problem
alert_duck(daffy)  # No problem
alert_bird(daffy)  # No problem for python, but problem for mypy, because daffy is a Duck, but not a Bird. However, for python, since Duck is subclass of Bird, it does not have a problem with it.

woody = Bird()
alert(woody) # Python problem: Bird has no attribute quack
alert_duck(woody) # Mypy problem: argument 1 to alert_duck has incompatible type Bird, expected Duck
alert_bird(woody)
```