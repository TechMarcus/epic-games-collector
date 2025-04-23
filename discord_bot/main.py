import json, datetime
from bot import discord_bot


def main():
    if datetime.datetime.today().weekday() != 3:
        return
    data = json.loads(open('../games_info.json').read())
    discord_bot(data)



if __name__ == '__main__':
    main()