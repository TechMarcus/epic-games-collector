from games_collector import EgsAccount, multi_collector
import json, datetime, os

def main():
    if datetime.datetime.today().weekday() != 3:
        return
    test_user = EgsAccount(user=os.getlogin())
    test_user.single_collector()
    # with open("accounts.json", "r") as f:
    #     accounts = json.load(f)
    # multi_collector(accounts)

if __name__ == "__main__":
    main()