use std::fs::File;
use std::io::ErrorKind;

fn main() {
    let filename = "white_rabbit.txt";
    let greeting_file_result = File::open(filename);

    let greeting_file = match greeting_file_result {
        Ok(file) => file,
        Err(error) => match error.kind() {
            ErrorKind::NotFound => match File::create(filename) {
                Ok(fc) => fc,
                Err(e) => panic!("Probrlem creating the file: {:?}", e),
            
            },
            other_error => {
                panic!("Problem opening the file: {:?}", other_error);
            },
        },
    };
}
