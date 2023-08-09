# Object-Oriented Programming features

## Object definition

```quote
Object-oriented programs are made up of objects. An object packages both data and the procedures that operate on that data. The procedures are typically called methods or operations.
```
So, rust's structs and enums provides the data structure and the `impl` blocks provide methods.

## Encapsulation

Rust provides enpapsulation because the default behavior of a struct is to be private to external code, and public data must be labeled with the `pub` keyword. Even if a struct is public, its fields are private by default as well. What gives the ability to create a public API to modify the private fields.

## Inheritance

Inheritance is a mechanism whereby an object can inherit elements from another object’s definition, thus gaining the parent object’s data and behavior without you having to define them again.

If a language must have inheritance to be an object-oriented language, then Rust is not one. There is no way to define a struct that inherits the parent struct’s fields and method implementations without using a macro.

However, you can use inheritance like features with traits, as seen in chapter 7

## Polymorphism

Rust uses generecis to abstract over different possible types and trait bounds to impose contraints on what those types must provide. See example in the gui folder.

In that example we define the Screen's components as a `Vec<Box<dyn Draw>>`, where `Box<dyn Draw>` is a trait object that can hold any type that implements the Draw trait. This is different of using `Vec<T>` because this would mean that the vector could only hold one type at a time, but `Box<dyn Draw>` could be a `Box<Button>`, a `Box<TextField>` or anything. This is a example of duck typing, i. e., if walks like a duck and quacs like a duck, then it's a duck.

Another way Rust provides polymorphism is using enums, that can be more than one type, that are known at compile time.



