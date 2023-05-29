package main

import (
	"fmt"
)

func main() {
	x := 10

	if x > 5 {
		fmt.Printf("x is big\n")
	} else {
		fmt.Printf("x is not big\n")
	}

	n := 2

	switch n {
	case 1:
		fmt.Println("one")
	case 2:
		fmt.Println("two")
	case 3:
		fmt.Println("three")
	default:
		fmt.Println("default")
	}
}
