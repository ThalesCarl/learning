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

# Testing flux control

Use `cargo test -- --something` to pass something to the test.

Tests are run in parallel. So, dont use the same resources and dont make the tests depend on each other.

To run test in serial mode: `cargo test -- --test-threads=1`

Any output that goes to stdout is not printed if the test passes. If you want to enable it, use `cargo test -- --show-output`

If you want to filter the tests from a suite of test, you can pass the test name or a part of it the CLI: `cargo test test_name`. If more than one test matches the string passed, they are run as well.

You can also ignore a test putting the annotation `#[ignore]` after the `[test]` annotation. On the other hand, you can run just the ignored tests using `cargo test -- --ignored`. And also, you can use `cargo test -- --inclede-ignored` to run all tests.

# Test organization

Rust community divides tests into unit tests and integration tests.

## Unit tests

Generally, they are placed in the same file that the function that is being tested is declared. The `#[cfg(test)]` ensures that the snippet will only be compiled when using `cargo test` and not when using `cargo build`.

Testing private functions are possible in rust.

## Integration tests

They are placed in a separeted `tests` folder in the root of the directory. Each file is a separeted crate, so we need to bring the `use` keyword to bring the test into scope.
We do not need to add `#[cfg(test)]` to the integration tests

The integration tests are only be run if all unit tests passing.

To create a module with common code to be used by all test, place them in `test/common/mod.rs` using the old naming convention. In this way, the file will not be shown in the stdout of the tests.

You can't create integration tests for functions defined in `src/main.rs`. Therefore, it's recommended that those functions are defined in `src/lib.rs` and the main file only have a minimum code that call functions in the lib file.
