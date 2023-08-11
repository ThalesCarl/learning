# Where you can use patterns

## match arms

```rust
match VALUE {
    PATTERN => EXPRESSION,
    PATTERN => EXPRESSION,
    PATTERN => EXPRESSION,
}

// For example
let x: Option<i32>;
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

`match` expressions must be exhaustive, i. e., all possibilities must be covered. One way to ensure this is to use the `_` as the last arm to catch all possibility that was not covered.

## Conditional `if let` Expressions

This expression is a shorter way to write the equivalent of a `match` that only matches one case. Optionally, `if let` can have a corresponding `else` containing code to run if the pattern in the `if let` doesnt match.
The downside of using this expression is that the compiler doesnt check for exhaustiveness.

```rust
let age: Result<u8, _> "34".parse();

if let Ok(age) = age {
    println("{age} years old");
} else {
    println("couldnt get age");
}

```

## Loops with `while let`

Allows a loop to run as long as a pattern continues to match.

```rust
let mut stack = Vec::new();

stack.push(1);
stack.push(2);
stack.push(3);

while let Some(top) = stack.pop() {  // which one is the pattern? Some(top)
    println!("{}", top);
}
```

## In `for` loops

The value that directly follows the keyword `for` is a pattern

```rust
let v = vec!['a', 'b', 'c'];

for (index, value) in v.iter().enumerate() {
    println!("{} is at index {}", value, index);
}
```

## `let` statements

Even the creation of a variable involves pattern matching

```rust
let x = 5;

let PATTERN = EXPRESSION;

let (x, y, z) = (1, 2, 3);
```

## Function Parameters

Also function parameters are patterns

```rust
fn print_coordinates(&(x, y): &(i32, i32)) {
    println!("Current location: ({}, {})", x, y);
}

fn main() {
    let point = (3, 5);
    print_coordinates(&point);
}
```

# Refutabiliry: whether a pattern might fail to match

A refutable pattern is a pattern that might fail. For example, `if let Some(x) = a_value`, because `a_value` could be `None` and it would not match with the `Some(x)`

Function parameters, let statements, and for loops can only accept irrefutable patterns, because the program cannot do anything meaningful when values don’t match. The if let and while let expressions accept refutable and irrefutable patterns, but the compiler warns against irrefutable patterns because by definition they’re intended to handle possible failure: the functionality of a conditional is in its ability to perform differently depending on success or failure.

That mean that `if let x = 5 {}` will generate a compiler warning because x would never be None, because it's not of type Some.

Also, `match` arms must use refutable patterns, except for the last arm, which should match any remaining values with an irrefutable pattern.

# Pattern syntax

## Maching literals

Use this when you want an actions if it gets a particular concreate value.

```rust
    let x = 1;

    match x {
        1 => println!("one"),
        2 => println!("two"),
        3 => println!("three"),
        _ => println!("anything"),
    }
```

## Matching Named Variables

Named variables are irrefutable patterns that match any value. But beware, the match pattern produces a new scope that might shadow the variable definition.

```rust
    let x = Some(5);
    let y = 10;

    match x {
        Some(50) => println!("Got 50"),
        Some(y) => println!("Matched, y = {y}"),
        _ => println!("Default case, x = {:?}", x),
    }

    println!("at the end: x = {:?}, y = {y}", x);
    // Output
    // Matched, y = 5
    // at the end: x = Some(5), y = 10
```

## Multiple pattern

You can match more than one pattern in the `match` expression using the `|` syntax, which is an `or` operator.

```rust
    let x = 1;

    match x {
        1 | 2 => println!("one or two"),
        3 => println!("three"),
        _ => println!("anything"),
    }
    // Output: one or two
```

## Ranges of values

Same idea as before but with ranges. Use the `..=` syntax. Works only for `chars` and numeric values.

```rust
let x 5;

match x {
    1..=5 => println!("one through five"),
    _ => println!("somethign else"),
}
```

## Destructuring Values

### Structs

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 0, y: 7};

    let Point { x: a, y: b} = p; // Creates variables a and b from p
    assert_eq!(0, a);
    assert_eq!(7, b);
    
    // Equivalent short hand
    let Point { x, y } = p; // It will create the variable x and y

    //

    match p {
        Point { x, y: 0 } => println!("on the x axis at {x}"),
        Point { x: 0, y } => println!("on the y axis at {y}"),
        Point { x, y } => println!("on neither axis ({x}, {y})"),
}
```

### Enums

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn main() {
    let msg = Message::ChangeColor(0, 160, 255);

    match msg {
        Message::Quit => {
            println!("The Quit variant has no data to destructure.");
        }
        Message::Move { x, y } => {
            println!("Move in the x direction {x} and in the y direction {y}");
        }
        Message::Write(text) => {
            println!("Text message: {text}");
        }
        Message::ChangeColor(r, g, b) => {
            println!("Change the color to red {r}, green {g}, and blue {b}",)
        }
    }
}
```

## Ignoring Values

### Ignorig an Entire Value with `_`

```rust
fn foo(_: i32, y: i32) {
    println!("This code only uses the y parameter: {}", y);
}

fn main() {
    foo(3, 4);
}
```

This is usefull when implementing a trait's function, that requires a parameter you dont use. Also, avoids unused variable warnings.

### Ignoring parts of a value with a nested `_`

```rust
let mut setting_value = Some(5);
let new_setting_value = Some(10);

match (setting_value, new_setting_value) {
    (Some(_), Some(_)) => println!("Cant overwrite an existing customized value");
    _ => {
        setting_value = new_setting_value;
    }
}
```

I didnt get it why this is ignoring part of a value.

### Ignore unused variable with `_`

Just start a variable with `_` like `_x` and the warning for the unused variable will not be issued.


### Ignore remainings of a value with `..`

```rust
    struct Point {
        x: i32,
        y: i32,
        z: i32,
    }

    let origin = Point { x: 0, y: 0, z: 0 };

    match origin {
        Point { x, .. } => println!("x is {}", x), // Usefull when you just want x
    }

```

Also works with a tuple

```rust
fn main() {
    let numbers = (2, 4, 8, 16, 32);

    match numbers {
        (first, .., last) => {
            println!("Some numbers: {first}, {last}");
        }
    }
}
```

## Extra Conditional with Match Guards

A match guard is an `if` specified after the pattern in a `match` arm, that must also match for that arm to be chosen. Allow more complex ideas than the pattern alone.

```rust
let num = Some(4);

match num {
    Some(x) if x % 2 == 0 => println!("The number {} is even", x),
    Some(x) => println!("The number {} is odd", x),
    None => (),
}
```

The compiler doesnt try to check for exhaustiveness when a match guard expression is involved.

You can also use `|` operator together with the match guard. In this case the `if` will be a `and` operation perform after all the `or` operations.
```rust
let x = 4;
let y = false;

match x {
    4 | 5 | 6 if y => println!("yes"),
    _ => println!("no"),
}

// Outputs: no
```

## `@` binding

```rust
enum Message {
    Hello { id: i32 },
}

let msg = Message::Hello { id: 5};

match msg {
    Message::Hello {
        id: id_variable @ 3..=7,
    } => println!("Found an id in range: {}", id_variable);
    Message::Hello {
        id: 10..12=
    } => println!("Found an id in range: {}", id_variable);
    Message::Hello { id } => println("Found some other id: {}", id),
}
```

I didn't understand this and the relevance of this.

