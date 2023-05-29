#!/bin/bash
set -eu

echo "Enter 1st string"
read st1

echo "Enter 2st string"
read st2

if [ "$st1" \< "$st2" ]
then
    echo "$st1 is smaller than $st2"
elif [ "$st1" \> "$st2" ]
then
    echo "$st1 is greater than $st2"
else
    echo "The strings have the same length"
fi

#Concatenate strings
c=$st1$st2
echo $c

#Upper Case First Letter
echo ${st1^}

#Upper Case Whole Variable
echo ${st1^^}

#Upper Case Just Vogals
echo ${st1^^[aeiou]}

#Lower Case First Letter
echo ${st1,}

#Lower Case Whole Variable
echo ${st1,,}

#Lower Case Just Vogals
echo ${st1,,[AEIOU]}

