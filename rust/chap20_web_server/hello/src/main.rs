use std::net::TcpListener;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap(); // bind is anologous to new in other structs

    for stream in listener.incoming() {
        let stream = stream.unwrap();
        println!("Connection established");
    }
}
