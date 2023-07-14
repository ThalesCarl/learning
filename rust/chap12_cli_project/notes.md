# Accepting cli args

Use `std::env::args` to get valid unicode strings from the command line. To get strings that may be invalid use `std::env::args_os`.

Use `.collect()` to the return object of `env::args()` function to turn it into a collection such as a vector of strings. The `collect` function needs the annotation of the type of the return.

# Random notes

- it's convention to call a struct's method `new` if you expect it not to fail and `build` if it may fail.

# Questions:

- Why we don't add a `&` to the call of the `search` functions in the test one_result()? Since string literals are references also?


