# Closures

Closures are anonymous functions you can save in a variable or pass as arguments to other functions. 

The call to a closure is done using for example

```rust
some = Option(12);
some.unwrap_or_else(|| foo())
```
where `foo()` is a function defined someplace else. If the closure had arguments, it would be placed between the two vertical bars  `||`.

Closures can be defined similarly as functions, just changing the breackts `()` to the `||` symbol, but unlike functions, you don't need to type annotate all of it.

Once a closure is used with one type, you can't use it again with another type.

Like functions, you can pass a mutable or immutable reference to a closure, but if you pass the former you can't use the reference somewhere else while you still have a immutable reference.

```rust
let mut list = vec![1, 2, 3];
println!("Before defining closure: {:?}, list};

let mut borrows_mutably = || list.push(7);

println!("Before calling closure: {:?}, list}; // ERROR here: using a reference to list that already have a mutable refence

borrows_mutably();
println!("After calling closure: {:?}, list}; // NO ERROR bc the list reference is not used anywhere else.
```

Question: we do not need to indicate that the parameter of a closure is a reference?

This is usefull when spawning (creating and using) threads.

```rust
use std::thread;

fn main() {
    let list = vec![1, 2, 3]
    println!("Before defining closure: {:?}, list};

    thread::spawn(move || println!("From thread: {:?}, list))
        .join()
        .unwrap();
}
```

Notice that we need the `move` keyword even tough the `list` reference is immutable. This is needed in order to prevent losing the reference if the main thread finishes executing.


## Fn traits

The type of closure depends on which of the Fn traits it implement. Quoting the book:

1. *FnOnce* applies to closures that can be called once. All closures implement at least this trait, because all closures can be called. A closure that moves captured values out of its body will only implement FnOnce and none of the other Fn traits, because it can only be called once.
2. *FnMut* applies to closures that don’t move captured values out of their body, but that might mutate the captured values. These closures can be called more than once.
3. *Fn* applies to closures that don’t move captured values out of their body and that don’t mutate captured values, as well as closures that capture nothing from their environment. These closures can be called more than once without mutating their environment, which is important in cases such as calling a closure multiple times concurrently.

Question: the code in listing 13-9 would work just because `num_sort_operations` is a integer? Or because it's mutable. Because the closure definition didn't change so much.

# Iterators

Iterators allows you to perform some task on a seqeuence of items.

```rust
let v1 = vec![1, 2, 3]

let v1_iter = v1.iter(); // Just create the iterator object. It does nothing until you use it

for val in v1_iter {
    println!("Got {}", val);
}
```

## Iterator trait and `next` method

All iterators implement a trait named `Iterator` that is defined in the standard library and in this trait the most useful method is the `next` method

```rust
#[test]
fn iterator_demo() {
    let v1 = vec![1, 2, 3];

    let mut v1_iter = v1.iter();

    assert_eq!(v1_iter.next(), Some(&1));
    assert_eq!(v1_iter.next(), Some(&2));
    assert_eq!(v1_iter.next(), Some(&3));
    assert_eq!(v1_iter.next(), None);
```

Notice that we receive a `Some(&1)` which is a immutable reference wraped by the type `Some`. If you want a mutable reference you can use the `iter_mut` instead of `iter`. I didn't get the use of `into_iter`.

## Methods that consume the iterator

Iterators methods that call `next` are *consuming adaptors*  because calling them uses up the iteraotr.

```rust
#[test]
fn iterator_sum() {
    let v1 = vec![1, 2, 3];

    let v1_iter = v1.iter();

    let total: i32 = v1_iter.sum(); // sum() take ownership of the reference of v1_iter

    assert_eq!(total, 6);
```

## Methods that produce other iterators

*Iterator adaptors* are methods defined on the `Iterator` trait that don't consume the iterator. Instead, they produce different iterators by changing some aspect of the original iterator.

```rust
let v1: Vec<i32> vec![1, 2, 3];
v1_iter = v1.iter().map(|x| x + 1); // map() is iterator adapter, 

// Also the line above does nothing by itself we need to call some method on the operator to use it
let v2: Vec<_> = v1_iter.collect(); // collect() runs the iterator and stores its results to data structure specified

assert_eq!(v2, vec![2, 3, 4]);
```

