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

## References and borrowing

References is a way to access a variable in the heap without need to move back and forth the object. They can be mutable or immutable. But not both simultaneously. Also you can only have one mutable reference at a time.

```rust
let mut s = String::from("Wake up, Neo!");
let r1 = &s; // no problem
let r2 = &s; // no problem
let r3 = &mut s; // Problem here, because r1 and r2 are expecting that the reference was still immutable
println!("{}, {} and {}", r1, r2, r3); 
```
The problem only occurs because the `println` macro is using the three references at once. If the code is written as below there is no problem because r1 and r2 are used before the creation of r3 and they are not used anymore.

```rust
let mut s = String::from("Wake up, Neo!");
let r1 = &s; // no problem
let r2 = &s; // no problem
println!("{} and {}", r1, r2); 

let r3 = &mut s; // no problem
println!("{}", r3); 
```

## Dangling references

Beware of the scope of a variable when returing its refence. Rust will produce a error at the code below because of that.
```rust
fn dangle() -> &String { // dangle returns a reference to a String

    let s = String::from("hello"); // s is a new String

    &s // we return a reference to the String, s
} // Here, s goes out of scope, and is dropped. Its memory goes away.
  // Danger!
```
