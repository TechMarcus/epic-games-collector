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
	err = GameInfoToJson(freeGames, "/app/games_info.json")
	if err != nil {
		log.Fatal(err)
		return
	}
}
