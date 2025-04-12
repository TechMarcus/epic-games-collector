package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
)

type FreeGamesPromotions struct {
	Data FreeGamesPromotionsData `json:"data"`
}
type FreeGamesPromotionsData struct {
	Catalog FreeGamesPromotionsCatalog `json:"Catalog"`
}
type FreeGamesPromotionsCatalog struct {
	SearchStore FreeGamesPromotionsSearchStore `json:"searchStore"`
}
type FreeGamesPromotionsSearchStore struct {
	Elements []FreeGamesPromotionsElements `json:"elements"`
}
type FreeGamesPromotionsElements struct {
	Title              string                         `json:"title"`
	Price              FreeGamesPromotionsPrice       `json:"price"`
	UpcomingPromotions FreeGamesUpcomingPromotion     `json:"promotions"`
	KeyImages          []FreeGamesPromotionsKeyImages `json:"keyImages"`
}

type FreeGamesPromotionsKeyImages struct {
	Url string `json:"url"`
}
type FreeGamesUpcomingPromotion struct {
	UpcomingPromotionalOffers []FreeGamesUpcommingPromotionalOffers `json:"upcomingPromotionalOffers"`
}
type FreeGamesUpcommingPromotionalOffers struct {
	PromotionalOffers []FreeGamesPromotionalOffers `json:"promotionalOffers"`
}
type FreeGamesPromotionalOffers struct {
	StartDate        string                                     `json:"startDate"`
	DiscountSettings FreeGamesPromotionalOffersDiscountSettings `json:"discountSetting"`
}

type FreeGamesPromotionalOffersDiscountSettings struct {
	DiscountPercentage int `json:"discountPercentage"`
}
type FreeGamesPromotionsPrice struct {
	TotalPrice FreeGamesPromotionsTotalPrice `json:"totalPrice"`
}

type FreeGamesPromotionsTotalPrice struct {
	OriginalPrice int `json:"originalPrice"`
	DiscountPrice int `json:"discountPrice"`
}

func CheckFreeGame() ([]string, error) {
	var listurl = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=UA&allowCountries=UA"
	resp, err := http.Get(listurl)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	var freeGamesPromotions FreeGamesPromotions
	b, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	err = json.Unmarshal([]byte(b), &freeGamesPromotions)
	if err != nil {
		log.Fatal(err)
	}
	elements := freeGamesPromotions.Data.Catalog.SearchStore.Elements
	if err != nil {
		return nil, err
	}

	var elems []string
	var startDate string
	for _, element := range elements {
		newGames, startDates := UpcommingGames(element)
		if newGames != "" {
			elems = append(elems, newGames)
		}
		if element.Price.TotalPrice.DiscountPrice == 0 {
			elems = append(elems, element.Title)
			fmt.Println(GetGamePicture(element))
		}
		if startDate == "" {
			startDate = startDates
		}
	}

	if len(elems) != 0 {
		return elems, nil
	}
	return nil, fmt.Errorf("game not found")
}

func UpcommingGames(element FreeGamesPromotionsElements) (string, string) {
	if element.UpcomingPromotions.UpcomingPromotionalOffers == nil {
		return "", ""
	}
	upcommingPromotions := element.UpcomingPromotions.UpcomingPromotionalOffers
	for _, upcommingPromotion := range upcommingPromotions {
		promotionOffers := upcommingPromotion.PromotionalOffers[0]
		if promotionOffers.DiscountSettings.DiscountPercentage != 0 {
			return "", ""
		}
		if element.Price.TotalPrice.DiscountPrice == element.Price.TotalPrice.OriginalPrice {

			return element.Title, promotionOffers.StartDate
		}
	}
	return "", ""
}

func GamesToTxt(games []string, filepath string) error {
	fiWR, err := os.OpenFile(filepath, os.O_RDWR, 0644)
	if err != nil {
		fmt.Println("Error opening FiW", err)
		return err
	}

	defer func() {
		fiWR.Close()
	}()

	fileStat, err := fiWR.Stat()
	if err != nil {
		fmt.Println("Error getting stats", err)
		return err
	}

	if fileStat.Size() != 0 {
		scanner := bufio.NewScanner(fiWR)
		line := 0
		for scanner.Scan() {
			if line <= len(games) || scanner.Text() != games[line] {
				fiWR, err = os.OpenFile(filepath, os.O_RDWR|os.O_TRUNC, 0755)
				if err != nil {
					fmt.Println("Error opening FiW", err)
					return err
				}
				fiWR.WriteString(strings.Join(games, "\n"))
				fmt.Println(scanner.Text())
				fmt.Println(games[line])
				fmt.Println("New games added")
				break
			}
			line++
		}
		return nil
	}
	fmt.Println("File is empty")
	fiWR.WriteString(strings.Join(games, "\n"))
	return nil
}

func GetGamePicture(element FreeGamesPromotionsElements) error {
	gamePicture := element.KeyImages[0].Url
	url := gamePicture

	response, e := http.Get(url)
	if e != nil {
		log.Fatal(e)
	}
	defer response.Body.Close()

	file, err := os.Create("../games_info/gamesPictures/" + element.Title + ".jpg")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	_, err = io.Copy(file, response.Body)
	if err != nil {
		log.Fatal(err)
	}
	return nil
}
