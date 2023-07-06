# Writing tests

A test is a function with a decorator `#[test]` on top of it.

```rust
#[test]
fn it_works() {
    let result = add(2, 2);
    assert_eq!(result, 4);
}
```

## Checking results

The `assert!` marcro evaluetes a boolean expression and panincs if the result is false. 

The `assert_eq!` macro takes two arguments and check if they're equal and `assert_ne!` is similar but with inequality. In order to use them in `structs` and `enums`, you need to implement the `PartialEq` trait and in order to print them correctly if the assertion is false, you need also to implement the `Debug` trait.

## Custom failure meesages

Just like python you can provide an extra argument to the assertion functions with the message to display in case the assertion is false

```rust
pub fn greeting(name: &str) -> String {
    String::from("Hello!")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greeting_contains_name() {
        let result = greeting("Carol");
        assert!(
            result.contains("Carol"),
            "Greeting did not contain name, value was `{}`",
            result
        );
    }
}
```

## Creating panics and chaos

```rust
fn create_chaos(input: i32) {
    if input > 10 {
        panic!("CHAOS");
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic]
    fn greather_than_10() {
        create_chaos(11);
    }
}
```

When you pass the `#[should_panic]` directive to the test, it's expected that the function tested will call the `panic!` macro.

You can also pass a `expected` string to check if the panic created inside the function was the one you expected

```rust
#[test]
#[should_panic(expected = "something passed to the panic macro")]
fn test() {}
```

## Using Result type

```rust
#[cfg(test)]
mod tests {
    #[test]
    fn it_works() -> Result<(), String> {
        if 2 + 2 == 4 {
            Ok(())
        } else {
            Err(String::from("2 + 2 = 5. Now repeat after me!"))
        }
    }
}
```

With this you use the `?` to make the testing more conveninent to write tests that should fail if any operation within them returns an `Err` variant.

However, with the Result type you can't use the `#[should_panic]` annotation.

Furthermore, in order to assert that an operation return an `Err`, don't use `?`. Use `assert!(value.is_err())` instead.
