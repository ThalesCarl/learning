#!/bin/bash

#save stdout and stderr to txt files
ls -al 1>stdout.txt 2>stderr.txt

#save stdout and stderr to the same file (trunc mode)
ls -al >log.txt 2>&1

#save stdout and stderr to the same file
#same as before but with different syntax
ls -al >& log.txt
 
#save stdout and stderr to the same file(append mode)
ls -al >>log.txt 2>&1
