# Generic Data Types

The generic data type works like templates in C++. 

## Functions 
To use it on the definition of a function place it inside `<>`

```rust
fn generic<T>(param1: T) -> T {}
```

Take a look at `largest` folder to get a complete example.


## Structs

```rust
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let integer = Point {x: 5, y: 10 };
    let float = Point {x: 1.0, y: 3.0 };
    let wrong = Point {x: 5, y: 2.0}; // it wont work bc x and y are the same type T.
                                      // to solve this use Point<T, U> {x: T, y: U}
}
```

## Enums

One example of use of generics is the Result enum used before

```rust
enum Result<T, E> {
    Ok(T), // holds a generic value T
    Err(E), // holds a generic error E
}
```

## Method implementation

Assuming the Point struct declared above, we can define a method that returns the value o `x`
```rust
impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}
```

Notice that the `<T>` comes also after the `impl` keyword.

Also, we can implement methods only for a specific type of the generic struct

```rust
impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}
```
