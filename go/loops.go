package main

import (
	"fmt"
)

func main() {
	for i := 0; i < 3; i++ {
		if i < 1 {
			continue
		}
		if i > 1 {
			break
		}
		fmt.Println(i)
	}
}
