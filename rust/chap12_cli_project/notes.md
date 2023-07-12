# Accepting cli args

Use `std::env::args` to get valid unicode strings from the command line. To get strings that may be invalid use `std::env::args_os`.

Use `.collect()` to the return object of `env::args()` function to turn it into a collection such as a vector of strings. 
