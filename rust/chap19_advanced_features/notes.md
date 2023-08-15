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
