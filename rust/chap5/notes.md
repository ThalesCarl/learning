# Structs

## Definition example
```rust
struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}
```
## Usage example

```rust
fn main() {
        let user1 = User {
        active: true,
        username: String::from("simas"),
        email: String::from("simas@turbo.com"),
        sign_in_count: 1,
    };
}

If the struct is mutable, the whole struct is mutable. We can choose fields to be mutable or constant.

## Field init shorthand

```rust
fn build_user(email: String, username: String) -> User {
    User {
        active: true,
        username,
        email,
        sign_in_count: 1
    }
}
```

This way you don't need to repeat `email: email` in the creation of the struct. 

I wonder if you can put in a different order than the definition order?

## Struct update syntax

Use this when you want to create a new instance only change some of the attributes

```rust
let user2 = User { 
    email: String::from("anotheremail@turbo.com"),
    ..user1 // Must be the last argument
};
```

Because we moved the username (which is a String) from user1 to user2, user1 is no longer available :(

## Tuple Structs

They are simple structs that does not have a name for their fields but have a name for the struct. For example:

```rust
struct Color(i32, i32, i32);

let black = Color(0, 0, 0);
```

## Unit-Like structs

They are struct that have no field. I didn'r find them very usefull so far.

```rust
struct AlwaysEqual;
let subject = AlwaysEqual;
```

## Ownership

You can only use references as types in rust if you use lifetimes, which is a concept we didnt see yet

## Methods

```rust
struct Rectangle { 
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50, 
    }
    let area = rect1.area();
}
```

`&self` is shorthand for `self: &Self`, which is also an alias to `rectangle: &Rectangle`

### Methods with more parameters

```rust
impl Rectangle {
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.with > other.with && self.height > other.height
    }
}
```

## Associated functions

They are functions (not methods) defined inside the `impl` block and that don't use the `self` argument. In general they are used to create a specific new type of the struct. For instance:

```rust
impl Rectangle {
    fn square(size: u32) -> Self {
        Self {
            width: size,
            height: size,
        }
    }
}

let sq = Rectangle::square(3);
```

## Questions:

* Structs are allocated on the heap or on the stack?
* It seems that methods don't have a signature close to the struct definition. How do we organize big structs?



