fn main() {
    let s1 = gives_ownership(); // Receives value from the function

    let s2 = String::from("Wake up"); // s2 comes into scope
    let s3 = takes_and_gives_back(s2); // s2 is moved into the function and it is moved backafter
} // s1 and s3 are droped and s2 was already moved

fn gives_ownership() -> String {
    // this function will move its return value into the function that calls it

    let some_string = String::from("yours"); // some_string comes into scope

    some_string // some_string is returned and moves out to the calling function
}

fn takes_and_gives_back(a_string: String) -> String { // a_string comes into scope
    a_string // a_string is returned and moves out to the calling function
}
