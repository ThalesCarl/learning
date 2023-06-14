# Growing projects

- Packages: A Cargo feature that lets you build, test, and share crates
- Crates: A tree of modules that produces a library or executable
- Modules and use: Let you control the organization, scope, and privacy of paths
- Paths: A way of naming an item, such as a struct, function, or module

## Packages and crates

Crates is the smallest amount of code that the Rust compiler considers at a time.

Crates can be:
- a binary crate: programs that are compiled to an executable. Must have a main function
- a library crate: functions that will be shared. Don't have a main function

A package is a bundle of one or more crates that provides a set of functionality. Must have at most one library crate and as many binary crates as you like.

By default, cargo knows that a binary crate will have a `src/main.rs` file and a library crate will have a `src/lib.rs` file.

A package can have multiple binary crates by placing files in the src/bin directory: each file will be a separate binary crate.

## Modules

Modules let us organize code within a crate. Modules control the privacy. Modules code is private by default. Use `pub` keyword to let the module's code public.

Modules seems to work like C++ namespaces

## Paths

To call a function we need to know its path. They can be:

- an absolute path: starts with the implicit `crate` and goes all the way to the function
- a relative path: starts in the current module and use `self`, `super` or other identifier to find the function

## Privacy of data types

Structs can have the fields public or private. Enums once declared as public, all the items are public as well.

## Bringing path into scope with the `use` keyword

This works like the `using` keyword in C++. Once you declare that you are using something you dont have to use all the :: identifier.

```rust
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

use crate::front_of_house::hosting; // Shouldnt be placed inside the eat_at_restaurant function?

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();
}
```

Like python you can use the keyword `as` to rename a module/struct/enum if you want to do it.


