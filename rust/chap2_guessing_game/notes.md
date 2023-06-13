Updating crate.io took two minutes on a connection with 2Mb/s download

I am not sure if I got right the concept of the Cargo.lock file. If I have specified `rand =0.8.5` in the Cargo.toml in the first time I build the project, it will create a `Cargo.lock` file with that version, but in the above paragraph it said that because of the `Cargo.toml` it would download the latest crate of the version `0.8.X`. It will download but it will not be used.  Blagh, it was explaind in the follwing section


match is good for avoiding the if else chain, and you have to treat every possibility of the Enum

functions does not make a implicit copy, therefore you have to pass a reference, because otherwise you will not have the variable after the return of the function
