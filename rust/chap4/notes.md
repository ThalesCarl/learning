# Understainding ownnearship

## Heap vs stack
Stack is fast and fixed size

Heap is slow but you don't need to know the size at compile time.
The pointer to a data stored in the heap can/should be placed in the stack, because you know it's size. Ownearship is responsible for keeping track of what parts of the code are using data on the heap, minimizing the amount of duplicate data on heap and cleaning up unused data on the heap.

## Ownership rules

1. Each value in Rust has an owner;
2. There can only be one owner at a time;
3. When the owner goes out of scope, the value will be dropped.

## String type

String literals are different data type of the `String` type? Yes, string literals are hardcoded chars sequence.

Rust's `drop()` function is called implicitly when a variable goes out of scope. It works like a C++ destructor.

The String data type is composed of (stored in the stack)::
* ptr: the pointer of the data in the heap;
* len: how much memory the contents are using, in bytes;
* capacity: the amount of memory that the String object has received from the allocator, also in bytes.

```rust
let s1 = String::from("Wake up");
let s2 = s1;

println!("{}, Neo!, s1); // s1 is no longer valid here, because it was moved to s2
```

This is similar to a shallow copy, but you don't end up with two pointers to the same heap data because, s2 is invalidated;

Also, Rust will never automatically create "deep" copies of the data. Hence, any automatic copy of the data is inexpensive.

## Cloning

In order to really deep copy a variable (with duplication of the heap data) you need to use the function `clone()`

```rust
let s1 = String::from("Wake up");
let s2 = s1.clone(); // deep copy here

println!("s1 = {}, s2 = {}", s1, s2);
```

## Copy trait 

Variables stored in the stack (integers, booleans, floats, char, tuples of know size) implement the `Copy` trait that indicates that the objects can be copied deeply without worries.

## Functions

See examples in this folder.

Notice that without using references, you would need to move a String variable into and from afterwards everytime you define a function like this

```rust
fn main() {
   let s1 = String::from("Wake up");

   let (s2, len) = calculate_length(s1);
}

fn calculate_length(s: String) -> (String, usize) {
    let length = s.len();
    (s, length)
}
```
