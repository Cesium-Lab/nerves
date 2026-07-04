fn greet(name: &str) { println!("Hello, {name}!"); }

// No semicolon = return value
fn add(a: i32, b: i32) -> i32 { a+b }

// return types like python
fn check_even(num: i32) -> bool { num % 2 == 0 }

fn main() {
    greet("Alice");

    let result = add(5, 3);
    println!("5 + 3 = {result}");

    let is_even = check_even(4);
    println!("4 is even: {is_even}");
}

