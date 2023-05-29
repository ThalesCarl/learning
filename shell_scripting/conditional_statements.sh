#!/bin/bash

count=10
if [ $count -eq 9 ] # Don't forget the space after [ and before ]
then
    echo "The condition is true"
elif (( $count >  9 )) # To use > sign double brackets are needed
then
    echo "The second condition is true"
else
    echo "The condition is false"
fi

: '
-eq equal
-ne not equal
-gt greater than
-ge greater than or equal to
-lt less than
-le less than or equal to
-a AND operator
-o OR operator
'

# Second example

age=61
if [ $age -ge 18 ] && [ $age -le 60 ] #AND operator
then
    echo "User is an adult!"
elif [[ "$age" -lt 18  ||  "$age" -gt 60 ]] # OR operator
then
    echo "User is not and adult"
fi

: '
double brackets is used when two comparissons are made
using double quotes around variables to ensure something
'


# Case example

echo -n "Enter the name of a country: "
read COUNTRY

echo -n "The offical language of $COUNTRY is "

case $COUNTRY in 
    Brazil)
        echo "Portuguese"
        ;;
    Italy | "San Marino" | "Vatican City")
        echo "Italian"
        ;;
    *)
        echo "unknow"
        ;;
esac
