import discord,os
import os


def discord_bot(games_data):
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$zig'):
            for game in games_data:
                await message.channel.send(game['Name'] + ' ' + game['Picture'])

    client.run(os.environ.get('DISCORD_TOKEN'))
