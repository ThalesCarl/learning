package main

import (
	"fmt"
)

func main() {
	book := "Espadachim de Carvão"
	fmt.Println(book)
	fmt.Println(len(book))

	fmt.Printf("book[0] = %v (format %T)\n", book[0], book[0])
	fmt.Printf("book[19] = %v (format %T)\n", book[19], book[19])
}
