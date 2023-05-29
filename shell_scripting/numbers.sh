#!/bin/bash
set -eu

echo 31+21 #concatenate strings, so no math is done

#To perform math, variables are needed

n1=4
n2=3

echo $(( n1 + n2 ))

#Other option
echo $(expr $n1 + $n2 )

#Convert Hex to Decimal number
HEX=AA
echo "obase=10; ibase=16; $HEX" | bc

#Floating point division, scale is the precision
echo "scale=2; 20+5/2" | bc
