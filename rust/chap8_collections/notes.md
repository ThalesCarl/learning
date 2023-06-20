# Common Collections

The collections that this chapter covers are stored in heap, which means we dont need to know their size beforehand at compile time and can grow and shrink as the program runs.

## Vectors

You can create a vector by one of the two following methods
```rust
let v: Vec<i32> = Vec::new();
let v = vec![1,2,3]; // Rust will infere that the data type is i32 because this is the default for integers
```

In order to update the vector you can use `push` method. Remember that a vector must be mutable in order to accept the addition of new elements

```rust
let mut v = Vec::new();

v.push(5); // Because we inserted a i32, rust will infer that that's the type of data we are using
```

```rust
let v = vec![1, 2, 3, 4, 5];

let third: &i32 = &v[2]; // Question: this is safe against core segmentation?
println!("Third = {third}");

let third: Option<&i32> = v.get(2);
match third {
    Some(third) => println!("Third = {third}),
    None => println!("Third is a lie!"),
}
```

Remember that `let third = &v[2]` is a immutable reference, and therefore you cannot modify the vector while it is still in the scope

Iteration in a vector can be done using

```rust
let v = vec![100, 32, 58];
for i in &v { // i is a immutable reference
    println!("{i}"); 
}
```

You can use also mutable references to change a element of the vector, but you cannot add or remove elements of the vector inside the for loop

```rust
let mut v = vec![100, 32, 57];
    for i in &mut v {
        *i += 50;
    }
}
```

You can use an enum to create a vector with different types in its elements

```rust
enum SpreadsheetCell {
        Int(i32),
        Float(f64),
        Text(String),
    }

    let row = vec![
        SpreadsheetCell::Int(3),
        SpreadsheetCell::Text(String::from("blue")),
        SpreadsheetCell::Float(10.12),
    ];
}
```

Because we will need a `match` to unpack this vector we can ensure that every possible case is handled at compile time.

## Strings

String is a collection of bytes. In rust strings are UTF-8.

In the core, there is only string slices `str`. The `String` is provided by the std library. 

You can create a string using the `new` method like you have used in the vector type or using the method `to_string` that is implemented that every type that implements the `Display` trait, as strings literals do.

```rust
// Creating
let mut s = String::new();

let data = "wake up, neo!";
let s2 = data.to_string();

// Updating
let mut s1 = String::from("foo");
s1.push_str("bar"); // push_str works with str slices
s1.push('!'); // push works only with a char type at a time

// Using + operator
let s1 = String::from("Wake up");
let s2 = String::from(", Neo!");
let s3 = s1 + &s2 // Returns a string, s1 is not longer valid and s2 is still valid

let s4 = format!("{s1}{s2}"); // Same as before, but more organized

// Indexing
let w = s1[0]; // This will not work because rust doesnt allow string indexing :(
let wake = s1[0..4]; // This is valid because it allows slicing but be carefull with this

// Iterating: you can choose between using the chars or the bytes of a String object

for c in "Зд".chars() {
    println!("{c}"); // Print З \n д
}
for b in "Зд".bytes() {
    println!("{b}"); // Print 208 151 208 180
}
```

## Hashmaps 

They work like a dictonary in python or a map in c++. They store their data in the heap. All keys must have the same type and all the values must have the same type.

```rust
use std::collections::Hashmap;

// Creating
let mut scores = Hashmap::new();

// Updating
scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Gray"), 50);

// Acessing elements
let team_name = String::from("Blue");
let score = scores.get(&team_name).copied().unwrap_or(0);
```

Here `get()` return an `Option<&V>` that is handled by the `copied()` function which transforms the `Option<&i32>` into a `Option<i32>` by coping its contents. After the function `unwrap_or` gets the value if the Option is Some or set to zero if None.

```rust
// Iterating

for (key, value) in &scores {
    println!("{key}: {value}");
}
```

For values with Copy trait, the values will be copied into the hashmap, for owned values like `String`, the object is moved into the hashmap, which becomes its owner. 

If you put references into a hashmap, you must ensure that they are still valid as long as the hashpap is valid. Wait, shouldnt the compiler do it for me?

### Updating a hashmap

You can:

- Overwrite a value

    ```rust
    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Blue"), 50);
    ```
- Add a key and value only if key isnt present
    ```rust
    scores.insert(String::from("Blue"), 10);
    scores.entry(String::from("Blue")).or_insert(50); // Will do nothing because Blue is already in use
    ```
- Update a value based on old value
    ```rust
    use std::collections::Hashmap;

    let text = "wake up wake";

    let mut map = Hashmaps::new();

    for word in text.split_whitespace() {
        let count = map.entry(word).or_insert(0); // Inst count immutable? Is this changing the map?
        *count += 1;
    }

    println!("{:?}", map);
    ```
