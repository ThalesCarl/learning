#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32
}

fn main() {
    // Get the area without using Struct
    let width1 = 30;
    let height1 = 50;

    println!(
        "The area of the rectangle is {}",
        area(width1, height1)
    );

    // Get the area using tuples
    let rec_tuple = (30, 50);
    println!(
        "The area of the rectangle is {}",
        area_tuple(rec_tuple)
    );

    // Get the area using struct
    let rec_struct = Rectangle {
        width: 30,
        height: 50,
    };
    println!(
        "The area of the rectangle is {}",
        area_struct(&rec_struct)
    );

    // println!("Debug rect: {:?}", rec_struct);
    dbg!(&rec_struct);
}

fn area(width: u32, height: u32) -> u32 {
    width * height
}

fn area_tuple(dimensions: (u32, u32)) -> u32 {
    dimensions.0 * dimensions.1
}

fn area_struct(rectangle: &Rectangle) -> u32 {
    rectangle.width * rectangle.height
}
