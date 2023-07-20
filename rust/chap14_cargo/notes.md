# Profiles

Cargo has two main profiles: dev and release. The dev is build when you use `cargo build` and the release is built when you use `cargo build --release`.

Cargo has default settings for the profiles, when you edit you `Cargo.toml` and add new settings, it will overwrite the default values. For example the default values for `opt-level` are

```rust
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

`opt-level` ranges from 0 to 3. More optimization takes longer to compile but the runtime is faster.

# Publishing to crates.io

As stated before, commenting with three slashse `///` in markdown will generate a html file in the `targer/doc` folder when you call the command `cargo doc`. Currently LaTeX is not fully supported, just using workarounds.

Commonly used sections are:
- Examples;
- Panics: where the function could panic
- Errors: possible errors that the function returns when using the `Result`
- Safety: if the functions is `unsafe` this is a description why

The `//!` is used to comment something within the definition, instead of just before like `///`.

When the crate structure is too complex, you can use the `pub use self::some_module::SomeStruct` syntax to list them in the beginning of the crate docuementaion.

To publish to crates.io you need to create a account (currently using github account is the method to create a new account). Once you have the account you can login using the API key on the command `cargo login <api_key>`

## Metadata

You need to provide some metadata to the package in order to publish it

```rust
[package]
name = "my_unique_name"
licence = "MIT" // A valid licence name accourding to SPDX
version = "0.1.0"
edtion = "2021" // Not really necessary
description = "Some meaningful description"
```

Finally, to publish it to `crates.io` registry, use `cargo publish`. Be carefull, because this is permanent. The version can never be overwritten and the code cannot be deleted.

To update new code to the same registry, just change the `version` metadata.

You cannot delete a version of the crate from the `crates.io` registry, but you can prevent any future project from adding them as a new dependency, by using `cargo yank --vers 0.1.0`. You can also undo this yankig using the `--undo` flag.
