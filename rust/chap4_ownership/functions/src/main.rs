fn main() {
    let s = String::from("Wake up"); // s comes into scope

    takes_ownership(s); // s's values moves into the function and so is no longer valid here
                        //
    println!("{}",s); // Causes error because s is no longer valid
    let x = 5;
    makes_copy(x); // x is copied into the function because i32 are allocated in the stack. You can still use x after here
} // Here, x goes out of scope, then s. But because s's value was moved nothing special haapnes.

fn takes_ownership(some_string: String) { // some_string comes into scope
    println!("{}", some_string); 
} // Here, some string goes out of scope and `drop` is called

fn makes_copy(some_integer: i32) { // some integer comes into scope
    println!("{}", some_integer);
} // Here, some_integer goes out of scope. Nothing special happens
