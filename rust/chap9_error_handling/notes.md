# Error Handling

Rust groups errors into *revocerable* and *unrecoverable*.

## Unrecoverable errors `panic!` macro

If this type of error occurs rust will print a failure message, unwind (walks back up the stack and cleans up the data) and quit. You can also abort, which ends the program without cleaning up.


To abort edit the `Cargo.toml` and insert:

```rust
[profile.release]
panic = 'abort'
```

You can explicit cause this type of error with the `panic!` macro.

```rust
fn main() {
    panic!("crash and burn");
}
```

## Recoverable errors with Result

Result is defined as

```rust
enum Result<T, E> {
    Ok(T), // T is the type of value that will be returned in case of success
    Err(E), // E is the of error that will be returned in case of failure
}
```

See `file_open_error` project to see the usage of the the Result type.

### unwrap

The `unwrap` method is a shortcut to return the `Ok´ value. If the Result is not Ok, `unwrap` will call the `panic!` macro.

```rust
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt").unwrap();
}
```
### expect

The `expect` is similar to `unwrap` but it let us choose the message of the `panic` macro
```rust
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt")
        .expect("hello.txt should be included in this project!");
}
```

## Propagating Errors

Use this when you just want to return the error to the caller of the function instead of handling with it

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let username_file_result = File::open("hello.txt");

    let mut username_file = match username_file_result {
        Ok(file) => file,
        Err(e) => return Err(e),
    };

    let mut username = String::new();

    match username_file.read_to_string(&mut username) {
        Ok(_) => Ok(username),
        Err(e) => Err(e),
    }
}
```

This pattern is so common that Rust provides the `?` operator to resume it

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut username_file = File::open("hello.txt")?;
    let mut username = String::new();
    username_file.read_to_string(&mut username)?;
    Ok(username)
}
```

The code above could be even more concise with

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut username = String::new();
    File::open("hello.txt")?.read_to_string(&mut username)?;
    Ok(username)
}
```

The operator `?` can only be used in functions whose return type is compatible, and by function is the outer function definition that returns a Result. Other type that are compatible are `Option` and any other method that implements `FromResidual` method. However, the `?` operator will not convert a Result into a Option and vice-versa. 

```rust

use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt")?; // Problem here
}
```

The above code will not compile because `main` returns a `()` and not a `Result`


## When to panic?

Question: I didnt get why defining the Guess struct is better than the other option presented, because we are calling `panic` and crashing the executable, when we could just recover like the other option. I agree we could define the Guess struct but then return a Err of a Result instead.
