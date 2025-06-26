from calendar import c
from encodings.punycode import T
from seleniumbase import SB

class EgsAccount:
    def __init__(self, user):
        self.user = user
    def single_collector(self):
        with SB(locale="en",headless=False,user_data_dir=rf'--user-data-dir=C:\\Users\\{self.user}\\AppData\\Local\\Google\\Chrome\\User Data\\') as sb:
            url = "https://store.epicgames.com/en-US/"
            sb.activate_cdp_mode(url)
            sb.sleep(5)

            collector(sb)

def multi_collector(accounts):
    for account in accounts:
        with SB(headless=False) as sb:
            sb.activate_cdp_mode("https://www.epicgames.com/id/login?lang=en-US&redirectUrl=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2F")

            sb.cdp.type("//*[@id='email']", account)
            sb.cdp.type("//*[@id='password']", accounts[account])
            sb.sleep(5)
            sb.cdp.mouse_click("button[type='submit']")
            sb.sleep(5)

            sb.cdp.open("https://store.epicgames.com/en-US/")
            collector(sb)


def collector(sb):
            sb.cdp.scroll_down(amount=300)
            try:
                free_games_position = sb.convert_xpath_to_css("/html/body/div[1]/div/div/div[4]/main/div[2]/div/div/div/div[3]/div[2]/span[1]")                
                sb.cdp.scroll_into_view(free_games_position)
            except:
                print("Free games not found by xpath")

            try:
                free_games = sb.cdp.find_elements('[data-component="FreeOfferCard"]')
                free_game_selector = '[data-component="FreeOfferCard"]'
            except TimeoutError: 
                free_game_selector = '[data-component="VaultOfferCard"]'
                free_games = sb.cdp.find_elements('[data-component="VaultOfferCard"]')

           
            for i in range(len(free_games)):
                try:                                 
                    free_game = sb.cdp.find_elements(free_game_selector)[i]
                    free_game.mouse_click()
                
                except:
                    print("Free game cant be found or clicked")
                    sb.sleep(5)
                    try: 
                        print("Trying to scroll into view")
                        sb.cdp.scroll_into_view(free_games_position)
                        sb.cdp.mouse_click(free_game)
                    except:
                        print("Free game cant be interacted")
                    break


                get_button_selector = "button[data-testid='purchase-cta-button']"
                sb.sleep(5)

                try:
                    sb.cdp.scroll_into_view(get_button_selector)
                    sb.sleep(10)
                except:
                    print("No get button")
                    sb.cdp.go_back()
                    continue

                if sb.cdp.get_text(get_button_selector) != "Get":
                    print("Not avalible to get")
                    sb.cdp.go_back()
                    continue

                sb.cdp.mouse_click(get_button_selector)
                sb.sleep(10)

                try:
                    iframe = sb.convert_xpath_to_css("/html/body/div[6]/iframe")
                    buy_button = sb.convert_xpath_to_css("/html/body/div[1]/div/div[4]/div/div/div/div[2]/div[2]/div/button")
                    sb.cdp.nested_click(iframe, buy_button) 
                except:
                    print("not logged in")
                    return
                
                print('Collected')
                sb.sleep(10)
                
                sb.cdp.open("https://store.epicgames.com/en-US/")
                sb.cdp.scroll_down(amount=300)
                sb.cdp.scroll_into_view(free_games_position)

                     


