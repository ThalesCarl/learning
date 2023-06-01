# Variables and constants

Variables are imutable by default. Add `mut` to allow them to change. Can I transform a variable immutable into mutable after I assign a value?

Constants are always immutable. Consts needs type annotation. Use keyword `const` to declare a constant. 

Shadowing a variable is giving a new value using the previous value, e. g.., x = x + 2.
If you use the `let` keyword for shadowing a variable, you are creating a new one, hence, you can change the type and the value using the previous values.

```rs
let spaces = "     ";
let spaces = spaces.len();
```

is different of 
```rs
let mut spaces = "     ";
spaces = spaces.len();
```

The second will produce a error because we are changing the variable type.

# Data types

## Scalars
Scalar are single value types: integers, floats, bools and characters.

I didn't get the integer integrals paragraph where the books says something about `57u8` as a declaration example

f64 is the default float

i32 is the default integer

char is unicode and has 4 bytes

## Compound Types

Group values into one type. Available are tuples and arrays.

Tuples have fixed length. The items of a tuple doesn't need to be the same type. Example: `let tup: (i32, f64, u8) = (500, 4.3, 1);`

To access the item of a tuple use: tup.0

Expressions return a empty tuple () always if not stated otherwise.


Arrays have fixed length. All the elements must be the same type. If you want to grow or shrink the collection you need to use the vector, that is provided by the standard library.

Declaration: `let a: [i32; 5] = [1, 2, 3, 4, 5]` 
For an array with the same value, you can use `let a: [3; 5]` that will create `a = [3, 3, 3, 3, 3]

Access array elements with the [];

# Functions

You must always specify the type of the parameter of a function.

Statements are instructions that perform some action and do not return a value;
Example: `let x = 5;` create the variable but the `let` is not assign to another variable
Hence, you can't do `x = y = 6;` in rust.


Expressions evaluate to a resultant value. They don't need a ending ;
Example:
```rust
let y = {
    let x = 3;
    x + 1
};
```
is valid and `y = 4`, but it's ugly as fuck.

The return values of functions are not named, but you need to specify their type like python 

```
fn plus_one(x: i32) -> i32 {
    x + 1
}
```

# Comments

Use double slash `//` everywhere. Style way is use comments almost always above the line and not in the end, even tough in the end are also acepptable.

Documentation comments use three slashes, but we will see them more down the road.
