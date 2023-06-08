fn first_word(s: &String) -> usize {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return i;
        }
    }
    s.len()
}

fn main() {
    let mut s = String::from("hello world");

    let word = first_word(&s);

    let mut first_word = String::from("");
    for (i, c) in s.chars().enumerate() {
        if i > word {
            break;
        }
        first_word.push(c);

    }
    println!("{}",first_word);
    s.clear();
    println!("{}", word); // Notice that even after clean the string word still can be used, and this is not good because the index does not correlate with the string anymore
}
