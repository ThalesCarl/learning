fn first_word(s: &String) -> &str{
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..] // Return the whole string if no space is found
}

fn main() {
    let mut s = String::from("hello world");

    let word_idx = first_word(&s);

    s.clear();
    println!("{}", word_idx); // Error here because word_idx is no longer valid after the clear method
}
