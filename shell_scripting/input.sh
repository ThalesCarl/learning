#!/bin/bash

#args passed by user
echo $1 $2 $3

#script name
echo $0

#all args in an array
args=("$@")

#print array elements
echo ${args[0]}
echo ${args[1]}

#print all array elements at once
echo $@

#print array length
echo $#

#read from a file
while read line
do
    echo "$line"
done < "${1:-/dev/stdin}"
