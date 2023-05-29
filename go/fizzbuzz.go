package main

import (
	"fmt"
)

func main() {
	for i := 1; i <= 20; i++ {
		fmt.Printf("%v ", i)
		if i%5 == 0 && i%3 == 0 {
			fmt.Printf("fizzbuzz")
		} else if i%3 == 0 {
			fmt.Print("fizz")
		} else if i%5 == 0 {
			fmt.Printf("buzz")
		}
		fmt.Printf("\n")
	}
}
