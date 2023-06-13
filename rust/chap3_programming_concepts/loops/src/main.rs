fn main() {
    let mut counter = 0;

    let result = loop {
        counter += 1;
        if counter == 10 {
            break counter * 2;
        }
    };
    println!("Counter: {counter}");
    println!("Result: {result}");

    for number in 1..4 {
        println!("Number: {number}");
    }

    let mut number = 5;
    while number < 8 {
        println!("Number: {number}");
        number += 1;
    }
}
