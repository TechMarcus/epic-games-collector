from calendar import c
from seleniumbase import SB
import time

class EgsAccount:
    def __init__(self, user):
        self.user = user
    def single_collector(self):
        with SB(uc=True, locale="en",chromium_arg=rf'--user-data-dir=C:\\Users\\{self.user}\\AppData\\Local\\Google\\Chrome\\User Data\\', headless=True) as sb:
            url = "https://store.epicgames.com/en-US/"
            sb.activate_cdp_mode(url)

            collector(sb)

def multi_collector(accounts):
    for account in accounts:
        with SB(headless=True) as sb:
            sb.activate_cdp_mode("https://www.epicgames.com/id/login?lang=en-US&redirectUrl=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2F")

            sb.cdp.type("//*[@id='email']", account)
            sb.cdp.type("//*[@id='password']", accounts[account])
            time.sleep(1)
            sb.cdp.mouse_click("button[type='submit']")
            time.sleep(5)
            collector(sb)


def collector(sb):
            try:
                free_games = sb.convert_xpath_to_css("/html/body/div[1]/div/div/div[4]/main/div[2]/div/div/div/div[2]/div[2]/span[7]/div/div/section/div")
            except:
                print("Free games not found by xpath")
            sb.cdp.scroll_into_view(free_games)
            sb.sleep(1)
            for i in range(1,5):
                try:
                    free_game = sb.convert_xpath_to_css(f"/html/body/div[1]/div/div/div[4]/main/div[2]/div/div/div/div[2]/div[2]/span[7]/div/div/section/div/div[{i}]")
                except:
                    # print("Free game not found by xpath")
                    break
                sb.cdp.mouse_click(free_game)
                time.sleep(4)

                get_button_selector = "button[data-testid='purchase-cta-button']"

                try:
                    sb.cdp.scroll_into_view(get_button_selector)
                except:
                    # print("No get button")
                    sb.cdp.go_back()
                    continue

                if sb.cdp.get_text(get_button_selector) != "Get":
                    # print("Not get")
                    sb.cdp.go_back()
                    continue

                sb.cdp.mouse_click(get_button_selector)
                time.sleep(7)

                try:
                    iframe = sb.convert_xpath_to_css("/html/body/div[6]/iframe")
                    buy_button = sb.convert_xpath_to_css("/html/body/div[1]/div/div[4]/div/div/div/div[2]/div[2]/div/button")
                    sb.cdp.nested_click(iframe, buy_button) 
                except:
                    print("not logged in")
                    return

                time.sleep(11)
                sb.cdp.refresh()
                sb.cdp.go_back()
                sb.cdp.go_back()
                sb.cdp.go_back()

                     


