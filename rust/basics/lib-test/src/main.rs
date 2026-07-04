use std::fs;
use std::path::PathBuf;

fn main() {
    // Path relative to src/main.rs
    let file_path = PathBuf::from(file!())
        .parent()
        .unwrap()
        .join("hello.txt");

    let contents = fs::read_to_string(&file_path).expect("Failed to read hello.txt");
    println!("File contents:\n{contents}");

    // let random_num: u32 = rand::random();
    println!("\nRandom number: {}", (random_num % 100) + 1);
}
