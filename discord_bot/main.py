import json
from bot import discord_bot


def main():
    data = json.loads(open('../games_info/games_info.json').read())
    discord_bot(data)



if __name__ == '__main__':
    main()