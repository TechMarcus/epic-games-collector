package main

import (
	"log"
)

func main() {
	freeGames, err := CheckFreeGame()
	if err != nil {
		log.Fatal(err)
		return
	}
	err = GameInfoToJson(freeGames, "../games_info/games_info.json")
	if err != nil {
		log.Fatal(err)
		return
	}
	// fmt.Println(freeGames)
	// fmt.Println("Program has finished. Press Enter to exit...")
	// fmt.Scanln()

}
