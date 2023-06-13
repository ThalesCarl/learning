fn main() {
    let s1 = String::from("Wake up");

    let len = calculate_length(&s1);

    println!("The length of {} is {}", s1, len);

    change(&s1); // This will produce an error, because it is trying to change a immutable reference
    change2(&mut s1); // This is fine. But remember that you can only have one mutable reference to a variable
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn change(s: &String) {
    s.push_str(", Neo!"); // This is trying to change a variable that is borrowed, which wil produce an error.
}

fn change2(s: &mut String) {
    s.push_str(", Neo!"); // This is trying to change a variable that is borrowed, which wil produce an error.
}
