#!/bin/bash

#While example
number=1
while [ $number -lt 10 ]
do
    echo "$number"
    number=$(( number+1 ))
done

#Until example (opposite of while)
n=1
until [ $n -ge 10 ]
do
    echo "$n"
    n=$(( n+1 ))
done

#For examples
for i in 1 2 3 4 5
do
    echo $i
done

for j in {0..20..2} # {start..end..increment}
do
    echo $j
done

for (( k=0; k<5; k++ ))
do
    echo $k

    if [ $k -eq 3 ]
    then
        break # continue is also available
    fi
done
