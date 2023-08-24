use std::{
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap(); // bind is anologous to new in other structs

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&mut stream);
    let http_request: Vec<_> = buf_reader // Vec<_> is using a placeholder to what collect() returns
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty()) // Checks if two lines in a row came empty? Or just one line came empty?
        .collect();

    println!("Request: {:#?}", http_request);
}
