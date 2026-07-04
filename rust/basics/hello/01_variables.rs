fn main() {
    // Variables are immutable by default (this is huge)
    let x = 5;
    println!("x = {}", x);

    let mut y = 10;
    println!("y = {y}");
    y = 15;
    println!("y after change = {y}");

    let z: i32 = 20;
    println!("z = {z}");

    let name: &str = "Rust";
    println!("Hello, {name}!");

    let pi: f64 = 3.14;
    println!("pi = {pi}");
}
