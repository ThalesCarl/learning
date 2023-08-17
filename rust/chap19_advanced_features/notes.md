# Unsafe rust

To switch to unsafe Rust, use the `unsafe` keyword and start a new block that holds the unsafe code.

The unsafe superpowers are:

* Deference a raw pointer;
* Call an unsafe function or method;
* Access or modify a mutable static variable;
* Implement an unsafe trait;
* Access fields of `union`s.

The `unsafe` keyword doesnt turn off the borrow checker or disable any other of the Rust's safety checks. You will stil get some degree of safety inside of an unsafe block. To isolate unsafe code, it's best to enclosure unsafe code within a safe abstraction and provide a safe API.

## Deferencing a raw pointer

A raw pointer is a new type of `unsafe` code and can be immutable (`*const`) and mutable (`*mut`). The asterisct is not the deference operator, it's part of the type name (WTF?). Immutable means that the pointer can't be directly assigned to after being deferenced. Different from references and smart pointers, raw pointers:

* Are allowed to ignore the borrowing rules by having both immutable and mutable pointers or multiple mutable pointers to the same location;
* Aren't guaranteed to point to valid memory;
* Are allwed to be null;
* Don't implement any automatic cleanup.

```rust
let mut num = 5;

let r1 = &num as *const i32;
let r2 = &mut num as *mut i32;

// Create a raw pointer to a arbitrary location in memory
let address = 0x01234usize;
let r = address as *const i32;

unsafe {
    println!("r1 is {}, *r1);
    println!("r2 is {}, *r2);
    println!("r is {}, *r);
}
```

## Calling an unsafe function or method

By declaring the function `unsafe` you tell the compiler to uphold the safe requirements and the user in the documentation to be careful. Inside the `unsafe` function there is no need to create another `unsafe` block.

```rust
unsafe fn dangerous() {}

// Calling dangerous outside an unsafe block is not okay
dangerous();

unsafe {
    dangerous(); // This is ok
}

```

Another example is presented below where we implement a way to split a slice in the middle

```rust
use std::slice;

fn split_at_mut(values: &mut [i32], mid: usize) -> (&mut [i32], &mut[i32]) {
    let len = values.len();
    let ptr = values.as_mut_ptr();

    assert!(mid <= len);

    unsafe {
        (
            slice::from_raw_parts_mut(ptr, mid), // Calls to unsafe function
            slice::from_raw_parts_mut(ptr.add(mid), len - mid), // .add() is also unsafe for raw pts
        )
    }
}
```

## Using `extern` funtions to call external code

Any code defined in another language is unsafe. The `extern` marks a block of code that will use an foreign ABI. To list availables ABI to integrate in rust use `rustc --print=calling-conventions`

```rust
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    unsafe {
        println!("Absolute value of -3 according to C: {}", abs(-3));
    }
}
```

On the other hand, we can define a Rust function as `external` to be able to call it from another language.

```rust
#[no_mangle] // Google mangling
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!"); // unsafe not required
}
```

## Accessing or Modifying a mutable static variable

The nemesis of every program language is also available in Rust: global variables. In rust they are called static variables.

```rust
static HELLO_WORLD: &str = "Hello, world!");

fn main() {
    println!("name is {}", HELLO_WORLD);
}
```

A `static` variable is similar to a `const` variable. They have `'static` lifetimes and should be named using `SCREAMING_SNAKE_CASE` by convention. Accessing immutable static variables is safe. But unlike constants variables, static variables have a fixed address in memory and can be mutable. However, it is `unsafe`

```rust
static mut COUNTER: u32 = 0;

fn add_to_count(inc: u32) {
    unsafe {
        COUNTER += inc;
    }
}

fn main() {
    add_to_count(3);

    unsafe {
        println!("COUNTER: {}", COUNTER);
    }
```

The above code works fine for single thread. For multiple threads, probably it could cause a data race.

## Implementing an Unsafe Trait

Just like functions, traits must be marked if are using `unsafe` code 

```rust
unsafe trait Foo {
    // methods definitions go here
}

unsafe impl Foo for i32 {
    // methods implementations go ere
}
```

## Accessing fields of an Union

A `union` is similar to a `struct`, but only one declared field is used in a particular instance at one time. Unions are primarily used to interface with unions in C code. Acessing union fields is unsafe because Rust can't guarantee the type of the data currently being stored in the union instance.


# Advanced traits

## Associated types

Traits with associates types have a type placeholder in the signature that can be filled when the trait is implemented rather in the definition.

```rust
pub trait Iterator { 
    type Item; // Associate type

    fn next(&mut self) -> Option<Self::Item>;
```

The `type Item` is the placeholder that must be filled in the implementation.

```rust
impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {}
```

It seems like a generics, but the difference is that with associated types we don't need to annotate types because we can't implement a trait on a type multiple times.

Question: what's the advantage of this then? The fact that we choose `Item = u32` makes no need to expecify the type everytime we create a Counter

## Default Generic Type Parameters and Operator Overloading

In rust you can't create your own operators or overload arbitrary operators. But you can overload the operation and corresponding traits listed in `std::ops`.

```rust
use std::ops::Add;

#[derive(Debug, Copy, Clone, Partial)]
struct Point {
    x: i32,
    y: i32,
}

impl Add for Point {
    type Output = Point; // Associate type

    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

// inside std::ops

trait Add<Rhs=Self> { // If Rhs is not defined, Rhs = Self = Point, which is the case
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

If we want to change the value of `Rhs` to make the sum of two different types, we can do as follow

```rust
use std::ops::Add;

struct Milimiters(u32);
struct Meters(u32);

impl Add<Meters> for Milimiters {
    type Output = Milimiters;

    fn add(self, other: Meters) -> Milimiters {
        Milimiters(self.0 + (1000 * other.0))
    }
}
```

Question: Rust couldnt figure out the type of the `Rhs` just by getting the type of the `other` parameter of the `fn add`?

## Disambiguation of traits methods

```rust
trait Pilot {
    fn fly(&self);
}

trait Wizard {
    fn fly(&self);
}

struct Human;

impl Pilot for Human {
    fn fly(&self) {
        println!("This is your captain speaking.");
    }
}

impl Wizard for Human {
    fn fly(&self) {
        println!("Up!");
    }
}

impl Human {
    fn fly(&self) {
        println!("*waving arms furiously*");
    }
}

fn main() {
    let person = Human;
    Pilot::fly(&person); // Out: This is your captain speaking.
    Wizard::fly(&person); // Out: Up!
    person.fly(); // Out: *waving argms furiously* . It could be Human::fly(&person) as well
}
```

## Fully qualified syntax

Also used for disambiguation of functions of traits and other objects.

```rust
trait Animal {
    fn baby_name() -> String;
}

struct Dog;

impl Dog {
    fn baby_name() -> String {
        String::from("Spot")
    }
}

impl Animal for Dog {
    fn baby_name() -> String {
        String::from("puppy")
    }
}

fn main() {
    println!("A baby dog is called a {}", <Dog as Animal>::baby_name());
}
```


## Supertrait: require one trait functionality within another trait

This is used when you want a trait implementation to require another trait.

It has the form: `trait NewTrait: RequiredTrait {}`. In order to implement the NewTrait in a type, you must implement the `RequiredTrait` first.

```rust
use std::fmt;

trait OutlinePrint: fmt::Display {
    fn outline_print(&self) {
        let output = self.to_string();
        let len = output.len();
        println!("{}", "*".repeat(len + 4));
        println!("*{}*", " ".repeat(len + 2));
        println!("* {} *", output);
        println!("*{}*", " ".repeat(len + 2));
        println!("{}", "*".repeat(len + 4));
    }
}

struct Point {
    x: i32,
    y: i32,
}

// In order to implement OutlinePrint to Point we need to implemen fm::Display first
impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

impl OutlinePrint for Point {}
```

## Breaking the orphan rule with Newtype pattern

The newtype pattern is a way to implement a external trait in a external type, thus breaking the orphan rule, using a wrapper

```rust
use std::fmt;

struct Wrapper(Vec<String>); // newtype pattern

impl fmt::Display for Wrapper {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[{}]", self.0.join(", "))
    }
}

fn main() {
    let w = Wrapper(vec![String::from("hello"), String::from("world")]);
    println!("w = {}", w);
}
```

The cat's jump (pulo do gato hueheuh) is that we use `self.0` to access the `Vec<T>` because `Wrapper` is a tuple struct.

The downside of using this technique is that `Wrapper` is a new type, so it doesnt have the methos of the value it's holding. We need to implement all the methods, or we can implement the `Deref` trait on the `Wrapper` to return the inner type.

# Advanced types

## More about the newtype pattern

The newtype pattern (`struct NewType(OldType)`) allows us to create a specific type from another type (kind of what `typedef` in C++). It is usefull to prevent mixing types and to hide internal implementation.

## Type aliases

The type aliases creates a synonym for another type. It is similar to newtype pattern but without enforcing that the type and the alias get mixed up

```rust
type Kilometers = i32; // type alias
struct Meters(i32); // newtype pattern

let x: i32 = 5;
let y: Kilometers = 6;
let z: Meters = 3;

println!("x + y = {}", x + y) // Ok
println!("x + z = {}", x + z) // Not Ok
```

It is usefull when you have a long type and want to make it shorter in th functions definition

## The Never Type 

We can create a function that never returns, aka diverging function. But because the function will never return, it needs a special operator to indicate it.

```rust
fn bar() -> ! {
}
```

I didn't get the applications of this.

## Dynamically sized type

TODO
