fn main() {
    let age = 18;
    if age >= 18 {
        println!("You are an adult");
    } else {
        println!("You are a child");
    }

    let num = 5;
    let result = if num > 0 { "positive" } else { "not positive" };
    println!("{num} is {result}");

    let mut count = 0;
    while count < 3 {
        println!("while count = {count}");
        count += 1;
    }

    for i in 1..=5 {
        println!("for i = {i}");
    }

    let mut x = 0;
    loop { // while loop
        println!("loop x = {x}");
        x += 1;
        if x >= 2 {
            break;
        }
    }
}
