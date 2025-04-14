from games_collector import EgsAccount, multi_collector
import asyncio
import os, json

with open("accounts.json", "r") as f:
    accounts = json.load(f)

def main():
    test_user = EgsAccount(user=os.getlogin())
    multi_collector(accounts)

if __name__ == "__main__":
    main()