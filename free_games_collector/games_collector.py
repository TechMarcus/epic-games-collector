from seleniumbase import SB
import time

class EgsAccount:
    def __init__(self, user):
        self.user = user
    def collector(self):
        with SB(uc=True, locale="en",chromium_arg=rf'--user-data-dir=C:\\Users\\{self.user}\\AppData\\Local\\Google\\Chrome\\User Data\\', headless=True) as sb:
            url = "https://store.epicgames.com/en-US/"
            sb.activate_cdp_mode(url)

            free_games = sb.convert_xpath_to_css("/html/body/div[1]/div/div/div[4]/main/div[2]/div/div/div/div[2]/div[2]/span[7]/div/div/section/div")
            sb.cdp.scroll_into_view(free_games)
            sb.sleep(1)
            for i in range(1,5):
                try:
                    free_game = sb.convert_xpath_to_css(f"/html/body/div[1]/div/div/div[4]/main/div[2]/div/div/div/div[2]/div[2]/span[7]/div/div/section/div/div[{i}]")
                except:
                    print("Free game not found by xpath")
                    break
                sb.cdp.mouse_click(free_game)
                time.sleep(4)

                get_button_selector = "button[data-testid='purchase-cta-button']"

                try:
                    sb.cdp.scroll_into_view(get_button_selector)
                except:
                    print("No get button")
                    sb.cdp.go_back()
                    continue

                if sb.cdp.get_text(get_button_selector) != "Get":
                    print("Not get")
                    sb.cdp.go_back()
                    continue

                sb.cdp.mouse_click(get_button_selector)
                time.sleep(7)

                iframe = sb.convert_xpath_to_css("/html/body/div[6]/iframe")
                buy_button = sb.convert_xpath_to_css("/html/body/div[1]/div/div[4]/div/div/div/div[2]/div[2]/div/button")

                sb.cdp.nested_click(iframe, buy_button) 
                time.sleep(10)

                sb.cdp.go_back()
            
            print("Done")