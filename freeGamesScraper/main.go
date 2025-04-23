package main

import (
	"fmt"
	"log"
	"time"
)

func main() {
	if time.Now().Weekday() != 3 {
		fmt.Println("Program can be run only on Wednesday")
		return
	}
	freeGames, err := CheckFreeGame()
	if err != nil {
		log.Fatal(err)
		return
	}
	err = GameInfoToJson(freeGames, "../games_info.json")
	if err != nil {
		log.Fatal(err)
		return
	}
	// fmt.Println(freeGames)
	// fmt.Println("Program has finished. Press Enter to exit...")
	// fmt.Scanln()

}
