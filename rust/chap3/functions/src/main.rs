fn main() {
    println!("Hello, world!");
    another_function(5,'m');

    let z = plus_one(7);
    println!("z is {z}");
}

fn another_function(x: i32, y: char) {
    println!("value of x is {x}{y}");
}

fn plus_one(x: i32) -> i32 {
    x + 1
}
