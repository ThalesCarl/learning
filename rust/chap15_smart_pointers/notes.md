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
