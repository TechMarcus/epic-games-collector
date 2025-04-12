from games_collector import EgsAccount
import asyncio
import os


def main():
    test_user = EgsAccount(user=os.getlogin())
    test_user.collector()

if __name__ == "__main__":
    main()