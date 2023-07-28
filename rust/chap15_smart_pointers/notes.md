Smart pointers are data structures that act like a pointer but also have additional metadata and capabilities. The difference of pointers and references is that while references only borrow data, in many cases, smart pointers own the data they point to. 

In rust smart pointers are usuall implemented using structs. Examples we have already met are Strings and Vec<T>. 

Smart pointers implement the `Deref` and `Drop` traits. 

The Deref trait allows an instance of the smart pointer struct to behave like a reference so you can write your code to work with either references or smart pointers. The Drop trait allows you to customize the code that’s run when an instance of the smart pointer goes out of scope.

# Box<T>

A `Box<T>` allow you to store data on the heap rather than the stack.

For simple types it behaves like a normal variable

```rust
fn main() {
    let b = Box::new(5);
    println!("b = {}", b);
} // when b goes out of scope, the data stored in the heap is deallocated as well
```

## Recursive types

Recursive types are types defined that can contain itself in the definition

```rust
enum List {
    Cons(i32, List),
    Nil,
}

let list = Cons(1, Cons(2, Cons(3, Nil))); //It won't work as it is, because the compiler can't know the size of Cons

// With Box
enum List {
    Cons(i32, Box<List>),
    Nil,
}

let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));

// It will work because the compiler knows the size of a Box<T>
```

# Deref trait

Allows to customize the behavior of the dereference operator `*`

```rust
fn main() {
    let x = 5;
    let y = Box::new(x); // Does new copy x's value to a new address in the heap? because x was stored in the stack

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

Implementing a `MyBox<T>` to understand the `Deref trait`

```rust
truct MyBox<T>(T); // What does this mean? Tuple struct!

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}

use std::ops::Deref;

impl<T> Deref for MyBox<T> {
    type Target = T; // not seen yet, more on chap19, but it's a generic parameter

    fn deref(&self) -> &Self::Target { // required by the Deref trait with this signature
        &self.0
    }
}

```
Now we can the `assert_eq!(5, *y)` like we did with Box<T>

Notice that we return a `&Self::Target` reference but we could have returned a different reference, like the `String` struct that returns a `&str`, this is called deref coersion. Let's see it in action

```rust
fn hello(name: &str) {
    println!("Hello, {name}");
}

fn main() {
    let m = Mybox::new(String::from("Rust));
    hello(&m); // &MyBox<String> -> &String -> &str because of deref coersion

    // Without deref coersion the code would look like
    hello(&(*m)[..]);
}
```

You can implement also the `DerefMut` to work with mutable references.

# Drop trait

Customize what the type do when it goes out of scope. Yeah, just like a destructor. For smart pointers `Drop` will deallocate the space in the heap that the box points to. 

`Drop` requires you to implement the function `fn drop(&mut self)`. Also, it is included in the prelude, so we don't need to bring it with `use` like we did for `Deref` trait.

Let's build another smart pointer to show the `Drop` trait implementation

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data '{}'!", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer {
        data: String::from("my stuff"),
    }
    let d = CustomSmartPointer {
        data: String::from("other stuff"),
    }
    println("CustomSmartPointers created");
}

// Output will be:
// CustomSmartPointers created
// Dropping CustomSmartPointer with data `other stuff`!
// Dropping CustomSmartPointer with data `my stuff`!
```

Sometimes, you may want to call the `drop` function early than the ending of the scope. For instace, when using a smart pointer that manages locks. In this cases, you can't call `drop` of the trait `Drop` manually, but you can use the `std::mem::drop` function that will call our `drop` function and most important will disable the aumatic insertion of `drop` when the value goes out of scope, preventing a double free bug. Also, `std::mem::drop` is also in the prelude, so you can call just `drop(your_var);`

```rust
fn main() {
    let c = CustomSmartPointer {
        data: String::from("some data"),
    };
    println!("CustomSmartPointer created.");
    drop(c);
    println!("CustomSmartPointer dropped before the end of main.");
}

// Output will be:
// CustomSmartPointer created.
// Dropping CustomSmartPointer with data `some data`!
// CustomSmartPointer dropped before the end of main.
```

# `Rc<T>`, the Reference Counted Smart Pointer


Usually, one value have just one owner, but there is some cases (e. g., nodes in a graph data structure) where the value shouldnt be cleaned up unless all the owners are gone.

The `Rc<T>` keeps a counter of the number of references in order to determine whether or not the value is still in use. If there are zero references to a value, the value can be cleaned up without any references becoming invalid.

As a smart pointer, `Rc<T>` will allocate memory on the heap, because we cant determine at compile time which part will finish using the data last. If we knew, we could just use regular ownership.

Note that `Rc<T>` is only valid for use in single-threaded scenarios.

```rust
enum List {
    Cons(i32, Rc<List>,
    Nil,
}

use crate::List::{Cons, Nil};
use std::rc::Rc;

fn main() {
    let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
    let b = Cons(3, Rc::clone(&a)); // Does not deep copy, just increase the reference count
    let c = Cons(4, Rc::clone(&a)); // It could be called a.clone(), but the convention is Rc::clone(&a)
}
```

`Rc::clone(&a)` creates the reference nad increases the reference counter. Note that `Rc<T>`'s `Drop` trait will decrease the reference counter.

`Rc<T>` only allow immutable references, because you would break the ownership rules with mutable references. In order to do that we will need to use `unsafe` stuff. Stick around!

# `RefCell<T>` and Interior Mutability Pattern

`RefCell<T>` behaves like a `Box<T>` but with the difference that it enforces the ownership rules at runtime instead of at compile time, which means that instead of getting a compile error when breaking the ownership rules, the program will panic and exit.

Notice that with this difference, using `RefCell<T>` will have a small penalty in performance because we will track the borrowing rules at runtime rather than compile time.

Similar to `Rc<T>`, `RefCell<T>` is only for use in single-threaded scenarios.

The include parameter to this type is `std::cell::RefCelli`

To get a mutable reference use the function `borrow_mut`, that will return a `RefMut<T>` smart pointer. On the other hand, use `borrow` to get an immutable reference, of the type `Ref<T>` smart pointer.

# Combining `Rc<T>` and `RefCell<T>` to allow multiple owners to mutable data. 


```rust
enum List {
    Cons(Rc<RefCell<i32>>, Rc<List>,
    Nil,
}

use crate::List::{Cons, Nil};
use std::cell::RefCell;
use std::rc::Rc;

fn main() {
    let value = Rc::new(RefCell::new(5));

    let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));

    let b = Cons(Rc::new(RefCell::new(3)), Rc::clone(&a));
    let c = Cons(Rc::new(RefCell::new(4)), Rc::clone(&a));

    *value.borrow_mut() += 10;

    println!("a after = {:?}", a); // value: 15
    println!("b after = {:?}", b); // value: (3, (15, Nil))
    println!("c after = {:?}", c); // value: (4, (15, Nil))
}
```

# References Cycles can leak memory 

A reference cycle occurs when the refernce count never hits zero and therefore the value will never be dropped.

Usually references circles happens when you have a `RefCell<Rc<T>>`.

References circles would not be caught either on compile time nor the first occurance in runtime. They will, instead, cause a overflow or consume all the memory available. 

## Preventing ref cycles by turning an `Rc<T>` into a `Weak<T>`

`Rc::clone` inscreases the `strong_count` of an `Rc<T>` and an `Rc<T>` is only cleaned up if its `strong_count` is zero.

To turn a `Rc<T>` into a `Weak<T>` call `Rc::downgrade()`. This will increase the `weak_count` of the `Rc<T>`. The `weak_count` is like the `strong_count` but doesnt need to be 0 for the `Rc<T>` to be cleaned up.

Because the value that Weak<T> references might have been dropped, to do anything with the value that a Weak<T> is pointing to, you must make sure the value still exists. Do this by calling the upgrade method on a Weak<T> instance, which will return an Option<Rc<T>>. You’ll get a result of Some if the Rc<T> value has not been dropped yet and a result of None if the Rc<T> value has been dropped.

```rust
use std::cell::RefCell;
use std::rc::Rc;

struct Node {
    value: i32,
    children: RefCell<Vec<Rc<Node>>>,
    parent: RefCell<Weak<Node>>, // If the children is droped the parent is not but not vice versa
}

fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        children: RefCell::new(vec![]),
        parent: RefCell::new(Weak::new()); // How does it know it is branch?
    }); 

    println!("leaf parent = {}", leaf.parent.borrow().upgrade()); 
    
    let branch = Rc::new(Node {
        value: 5,
        children: RefCell::new(vec![Rc::clone(&leaf)]),
        parent: RefCell::new(Weak::new());
    }); 

    *leaf.parent.borrow_mut() = Rc::downgrade(&branch); // The relationship is stablished here
    println!("leaf parent = {}", leaf.parent.borrow().upgrade()); 
    
```

