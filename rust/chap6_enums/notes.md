# Enums

## Definition

```rust
enum IpAddrKind {
    V4,
    V6
}

let four = IpAddrKind::V4;
let six = IpAddrKind::V6;
```

## Using enum types as functions

The name of each enum variant that we define also becomes a function that constructs an instance of the enum. A crazy concept indeed XD

```rust
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

let home = IpAddr::V4(127, 0 , 0, 1);
let loopback = IpAddr::V6(String::from("::1"));
```

I didn't get the following snippet 

```rust
enum Message {
    Quit, // where is the type? I know it's a unit struct but how do the compiler knows?
    Move {x: i32, y: i32}, // shouldn' be using () instead of {}?
    Write(String),
    ChangeColor(i32, i32, i32);
}
```

Enums also can use the `impl` keyword to define functions (?) like a struct:

```rust
impl Message {
    fn call(&self) {
        // call definition // how do I get the string passed to the constructor?
    }
}

let m = Message::Write(String::from("wake up, neo!");
m.call();
```


## The type Option

Important: rust does not have the `null` type by default, but you can define it with the enum `Option`

```rust
enum Option<T> {
    None,
    Some(T),
}
```

You don't even need to include `Option`, `None` or `Some` because they are so common that are included by default (in the prelude? wtf is that?). You can also drop the `Option::` prefix to invoke `None` and `Some`. Usage example:

```rust
let some_number = Some(5);
let some_char = Some('c');

let absente_number: Option<i32> = None; // Always need to type annotate the None type
```
In order to use `some_number` you will have to convert it to a valid value and treat the case where it could be null. This is the advantage of using `Option` over using a `null` concept.

# Match control flow construct

It work like a switch case but with any type of pattern (a pattern could be several things, more on chapter 18).

```rust
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }
}
```

The condition after the match is like the condition after the `if` keyword but it can be any pattern and not just a boolean like the `if` keyword.

## Matching with Option<T>

```rust
fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None, // Why are you returning None? if None cannot be used afterwards 
        Some(i) => Some(i + 1),
    }
}

let five = Some(5);
let six = plus_one(five);
let none = plus_one(None);
``` 

If we don't cover the case where Option could be None, the compiler would throw an error.

### Catch all placeholder _

```rust
let dice_roll = 7;
match number {
    3 => add_fancy_hat()
    7 => remove_fancy_hat(),
    _ => roll_again(), // Default case.
}
```

If you use `_` as the placeholder you usually don't pass that value to the function associated? On the other hand, it's  common to return a unit tuple `()` to the catch all placeholder

## if let

```rust
let config_max = Some(3);
if let Some(max) = config_max {
    println!("The maximum is configured to be {}", max);
}
```
The above code is the same as 
```rust
let config_max = Some(3u8);
match config_max {
    Some(max) => println!("The maximum is configured to be {}", max),
    _ => (),
}
```

This is just a way to economize the exaustive checking of the match keyword.

You can also use a `else` in the `if let` construction when you want a piece of code to run with all the expressions that don't match the expected pattern.

```
let mut count = 0;
let config_max = Some(3);
if let Some(max) = config_max {
    println!("The maximum is configured to be {}", max);
} else {
    count += 1;
}
