package main

import (
	"fmt"
	"log"
)

func main() {
	freeGameName, err := CheckFreeGame()
	if err != nil {
		log.Fatal(err)
		return
	}
	err = GamesToTxt(freeGameName, "../games_info/currentGames.txt")
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(freeGameName)
	fmt.Println("Program has finished. Press Enter to exit...")
	fmt.Scanln()

}
