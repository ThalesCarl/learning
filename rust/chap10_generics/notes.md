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

# Traits

Syntax:

```rust
pub trait Summary {
    fn summarize(&self) -> String; // Notice the ;
}
```

Every type that has the trait Summary will have to implement the `summarize` function. See `traits` folder for a complete example.
You can implement a external trait in one of your types(like Display trait into MyType), or you can implement a local trait in a external type(like MyTrait into Vec<T>), but never you can implement one external trait into a external type. Thats the orphan rule, because the parent is not present (kind mean, isnt?). 

## Default implementations

Even tought we said before that every type needed to implement the functions of the trait, we can provide a standard implementation

```rust
pub trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")
    }
}
```

In order to use the default implementation, put this on your script `impl Summary for NewsArticle {}`

## Traits as parameters

You can use the trait as a parameter of a function and be able to pass a object that implements that trait into the function

```rust
pub fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}

pub main() {
    let tweet = Tweet {whaterver}

    notify(&tweet); // Is this the way we do polymorphisms?
}
```

## Trait bounds

But what if we need to ensure that in case of two parameters being passed to a function they have the same type. To do so we use

```rust
pub fn notify<T: Summary>(item1: &T, item2: &T ) { 
    println!("Breaking news! {} and {}", item1.sumMarize(), item2.summarize());
}
```

Not really useful in my opnion.

## Multiple trait bounds

Not sure if I got this one but here is the syntax

```rust
pub fn notify(item: &(impl Summary + Display)) { 

// With the generics
pub fn notify<T: Summary + Display>(item1: &T, item2: &T ) { 
```

To make it more easy to read  you can use


```rust
fn some_function<T, U>(t: &T, u: &U) -> i32
where
    T: Display + Clone,
    U: Clone + Debug,
{}
```

## Returning a trait 

You can also use this kind of systax to return a `impl Trait`. It seemed even less useful to me.

## Conditional  implemnt methods with Trait bounds

I didnt get this one.
```rust
use std::fmt::Display;

struct Pair<T> {
    x: T,
    y: T,
}

impl<T> Pair<T> {
    fn new(x: T, y: T) -> Self {
        Self {x, y}
    }
}

impl<T: Display + PartialOrd> Pair<T> {
    fn cmp_display(&self) {
        if self.x >= self.y {
            println!("x is largest!");
        } else {
            println!("y is largest!");
        }
    }
}
```

# Lifetimes

Lifetimes annotations dont change how long any of the references live. Rather, they describe the relationships of the lifetimes of multiple refernces to each other without affecting the lifetimes.

```rust
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

The lifetime annotation doesnt mean much thing by itself. They useful when they interact. Lets see an example:

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn main() {
    let string1 = String::from("long string is long");
    let result;
    {
        let string2 = String::from("xyz");
        result = longest(string1.as_str(), string2.as_str());
    }
    println!("The longest string is {}", result); // It wont compile bc the lifetime of the result is the same as the string2
}
```

## Strucs with references using lifetimes

```rust
struct ImportantExcerpt<'a> {
    part: &'a str,
}

fn main() {
    let novel = String::from("Holy hand grenade. Five!");
    let first_sentence = novel.split('.').next().expect("Could not find a '.'");
    let i = ImportantExcerpt {
        part: first_sentence,
    };
}
```

## Lifetime Elision (when lifetimes annotations are not necessary)

- when you have one input and one output reference like 
    `fn foo(s: &str) -> &str {}` // Does it work for any reference or just for str?
- when the input parameter is `&self` or `&mut self`

Rules:
1. The compiler assigns a lifetime parameter to each parameter that's a reference
    `fn foo(x: &str, y: &str)` becomes `fn foo<'a, 'b>(x: &'a str, y: &'b str)`
2. If there's only one input, its lifetime is assigned to all output lifetime parameters
3. If there's multiple inputs, but one of them is  `&self` or `&mut self`, the lifetime of `self` is assigned to all output lifetimes.

If the compile applies these rules and could not determine the lifetime by itself, it throws an error.

## Lifetime annotations in Methods Definitions

```rust
iml<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 { // Dont need to annotate lifetime because of third and first rule
        2
    }
}
```

## Static Lifetime

A lifetime is static when the reference is suppose to live for the entire execution of the program. Use `&'static to declare a refence static. But be carefull whit this. Sometimes you see an error of the compiler suggesting to make the reference static, but that's not always the solution. 

Also string literals `str` have always static lifetimes.


# Everything we saw put together

```rust
use std::fmt::Display;

fn longest_with_an_announcement<'a, T>(
    x: &'a str,
    y: &'a str,
    ann: T,
) -> &'a str
where
    T: Display,
{
    println!("Announcement: {}", ann);
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
```
