# Rust Basics

Learning the fundamentals of Rust on M1 Mac.

## Setup & Compilation

### [Install Rust](https://rust-lang.org/tools/install/)
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Compile & Run
```bash
# Compile and run in debug mode
rustc main.rs && ./main

# Or use Cargo (once projects are set up)
cargo run
```

### M1 Mac Notes
- Rust works natively on M1 — no special setup needed
- Binaries will compile to ARM64 by default

<!-- ## Topics to Cover

- [ ] Variables and mutability
- [ ] Data types (integers, floats, booleans, strings)
- [ ] Functions and control flow (if/else, loops)
- [ ] Ownership and borrowing
- [ ] Pattern matching
- [ ] **Type Hinting** — explicit type annotations (coming soon)
- [ ] **Libraries & Packages** — using external crates with Cargo (coming soon) -->


## Resources

- [The Rust Book](https://doc.rust-lang.org/book/) — official guide
- `rustc --explain E####` — look up specific compiler errors
