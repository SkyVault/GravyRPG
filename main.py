import atexit
import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

from game import Game
from player import Player

load_dotenv()

GUILD = 'Gamers North'

with open(".env", "r") as f:
    TOKEN = f.readline()

class TheClient(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.guild = None
        self.game = Game()

    async def on_ready(self):
        self.guild = discord.utils.get(self.guilds, name=GUILD)
        print(f'Logged in as {self.user.name}, {self.user.id}')

    async def on_message(self, message):
        if message.channel.name != 'gravy-rpg':
            return
        print(message, "\n", message.content)
        if message.content.startswith('!'):
            splits = message.content[1:].split(' ')
            await self.game.dispatch(message.author.id, splits[0], splits[1:], message)


client = TheClient()


def saveAtExit():
    client.game.save()


atexit.register(saveAtExit)
client.run(TOKEN)
