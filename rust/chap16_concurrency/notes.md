# Threads

We use `thread::spawn` to create a new thread and pass a closure to it, that will tell what will be run in the thread.

```rust
use std::thread;
use std::time::Duration;

fn main() {
    thread::spawn(|| {
        for i in 1..10 {
            println!("number {} in the spawned thread!", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("number {} in the spawned thread!", i);
        thread::sleep(Duration::from_millis(1));
    }
}
```

Notice that when the for in the main thread ends, the program will end neverthless the for in the spawned thread didnt finish.

## Waitnig for all threads to finish

We will use the `join` handle to make the program wait until the thread associated with the handle is done.

To do this associate a thread with a variable `let handle = thread::spawn(||{})` and then `handle.join().unwrap()`. 

Question: why do we need to call the `unwrap`? 

To pass a value to the thread, use the `move` keyword before the closure definition.

# Channels: Message passing to transfer data between threads

A channel is way to communicate between two things. If one part is no longer available, the channel is considered closed.

In the example below, we send a message from the spawned thread to the main thread. Obs: tx = transmiter, rx = receiver is the rust convention

```rust
use std::sync::mpsc; // mpsc = multiple producer, single consumer

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
        // After the send, val is no longer available.  
    });

    let received = rx.recv().unwrap(); // Blocks the main thread and wait until a value is sent
    println!("Got: {}", received);
}
```

The `rx` have two functions: `recv` and `try_recv`. The first blocks the thread and wait for a value. The second doesnt blocks the thread, but just return a `Ok` if there is one message available.
We can shorten the operation of the rx transforming it to an operator:

```rust
for received in rx {
    println!("Got: {}", received);
}
```
Question: does rx wait until all the values have been received before iterating? If yes, how does it know when to start?

## Using multiple producers

```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::channel();

    let tx1 = tx.clone();
    thread::spawn(move || {
        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("thread"),
        ];
    
        for val in vals {
            tx1.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }

    thread::spawn(move || {
        let vals = vec![
            String::from("more"),
            String::from("messages"),
            String::from("for"),
            String::from("you"),
        ];
    
        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
        for received in rx {
            println!("Got: {}", received);
        }
```

For channels, once a message is sent you have no longer the access to the its value in the sending thread. If you want to have multiple ownership (like we did in the smart pointers chapter) we need to use mutexes.

# Mutexes: shared memory concurrency

A mutex (mutual exclusion) allows only one thread to access some data at any given time.

A thread must first signal that it wants to access the data by acquiring the mutex's `lock`. The lock is a data struture that is part of the mutex that keeps track of who currently has exclusive access to the data.

To use the lock remember you must first attempt to acquire the lock before using the data and then you must unlock the data after using it.

In rust a Mutex is a shared pointer `Mutex<T>`. 

```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(5);

    {
        let mut num = m.lock().unwrap();
        *num = 6;
    } // The Drop trait unlocks the mutex automatically

    println!("m = {:?}", m);
}
```

## Sharing a `Mutex<T>` between multiple thread

We use the `Arc<T>` smart pointer to substitute a `Rc<T>` for concurrent programs. They have the same API. But, because of thread safety guarantees, arc is slower than Rc.  Arc = atomically reference counted. 

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();

            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: *counter.lock().unwrap());
}
```

The book doesnt explain how to prevent deadlocks :(

# Sync and Send traits

The `Send` marker trait indicates that the type can be sent between threads.

Almost every type in rust have the Send trait, except `Rc<T>` and some others

The `Sync` marker trait indicates that it is safe for the type to be referenced from multiple threads.

Primitive types have implemented `Send` and `Sync` traits, and types composed of primitives types also have them automatically.

We dont have to implement these traits manually in general. In order to do it, we will enter in the unsafe world of rust.
