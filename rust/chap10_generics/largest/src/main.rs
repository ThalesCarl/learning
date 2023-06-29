fn largest_without_generics(list: &[i32]) -> &i32 {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}

fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}


fn main() {
    let number_list = vec![34, 50, 25, 100, 43];
    
    let result = largest(&number_list);
    println!("The largest number is {result}");

    let char_list = vec!['a', 'b', 'y', 'd'];
    
    let result = largest(&char_list);
    println!("The largest char is {result}");
}
