fn main() {
    let s1 = String::from("Wake up");

    let len = calculate_length(&s1);

    println!("The length of {} is {}", s1, len);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn change(s: &String) {
    s.push_str(", Neo!"); // This is trying to change a variable that is borrowed, which wil produce an error.
}
