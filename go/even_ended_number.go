package main

import (
	"fmt"
)

func main() {
	count := 0
	for i := 1000; i < 10000; i++ {
		for j := i; j < 10000; j++ {
			n := i * j
			s := fmt.Sprintf("%d", n)
			if s[0] == s[len(s)-1] {
				count++
			}
		}
	}
	fmt.Println("count = %d\n", count)
}
