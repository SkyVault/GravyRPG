import threading, pickle, os, sys

from functools import reduce
from textwrap import dedent

from art import BANNER
from player import Player, State
from world import getUniverse
from discord.ext import tasks

def print_help(*args) -> str:
    return """
    
    start-new               - starts a new game
    rename <new-name>       - Renames your character in game
    self                    - Displays stats and information for your character
    locate                  - Displays the current location
    players                 - Displays all of the players
    inv                     - Displays the players invatory
    descr (ship|<item:id>)  - Displays the description of an item
    near (planet|system|galaxy) - Displays nearby things
    travel <planet:id>      - Start a trip to a planet
    map                     - Displays a list of places you can go on a planet/space-station
    """


def print_self(player) -> str:
    return str(player)


class Game:
    def __init__(self):
        self.players = {}
        self.commands = {
            "help": print_help,
            "self": print_self,
        }
        self.universe = getUniverse()
        self.lock = threading.Lock()
        self.load()
        self.main_loop.start()

    @tasks.loop(minutes=0.01)
    async def main_loop(self):
        for player in self.players.values():
            player.tick()

            await player.updateTargetMessage()

    def save(self):
        total = {"players": self.players, "universe": self.universe}
        with open("save", "wb") as f:
            pickle.dump(total, f)

    def load(self):
        if not os.path.exists("save"):
            self.save()

        with open("save", "rb") as f:
            res = pickle.load(f)
            print(res)
            self.universe = res["universe"]
            self.players = res["players"]

    async def dispatch(self, who, cmd, args, message) -> None:
        try:
            print(who, cmd, args)

            async def say(msg_):
                await message.channel.send(f"`{msg_}`")

            if who not in self.players:
                await say(BANNER)
                await say("Welcome new player! Just created your character")
                player = Player()
                earth, system, galaxy = self.universe.getPlanetByName("Earth")
                player.location = earth
                self.players[who] = player

            if cmd == "help":
                await say(print_help())
            elif cmd == "banner":
                await say(BANNER)
            elif cmd == "self":
                await say(print_self(self.players[who]))
            elif cmd == "rename":
                if len(args) == 0:
                    await say("Missing argument <name>")
                else:
                    pre = self.players[who].name
                    self.players[who].name = args[0]
                    await message.channel.send(f"renamed {pre} to {args[0]}")
            elif cmd == "map":
                pass
            elif cmd == "travel":
                player = self.players[who]
                if len(args) == 0:
                    await message.channel.send("Missing argument <planet:id>")
                    return
                elif player.spaceShip is None:
                    await message.channel.send(f"Cannot travel without a space ship...")
                else:
                    planet, _, _ = self.universe.getPlanetByName(args[0])
                    if planet is None or planet.name == "Unknown":
                        await message.channel.send(f"Cannot find planet {args[0]} in the records")
                        return
                    res = await message.channel.send(f"Traveling to {planet.name}...")
                    player.startTravel(planet, target_message=res)

            elif cmd == "locate":
                await say(self.players[who].locate(self.universe))
            elif cmd == "players":
                msg = reduce(lambda a, b: a.name + "\n" + b.name, self.players.values())
                await message.channel.send(f"Players:\n{msg}")
            elif cmd == "inv":
                player = self.players[who]
                ship = None
                if player.spaceShip is not None:
                    ship = f"{player.spaceShip.name}"
                msg = f"Space Ship: {ship}\nCargo: {player.inventory}"
                await message.channel.send(msg)
            elif cmd == "descr":
                if len(args) == 0:
                    await message.channel.send("Missing argument (ship|<item:id>)")
                else:
                    if args[0] == "ship":
                        player = self.players[who]
                        if player.spaceShip is None:
                            await message.channel.send(f"You don't own a space ship...")
                        else:
                            await message.channel.send(f"{player.spaceShip.name}:\n{player.spaceShip.descr}")
            elif cmd == "near":
                player = self.players[who]
                if len(args) == 0:
                    await message.channel.send("Missing argument (planet|system|galaxy)")
                else:
                    if args[0] == "planet":
                        subsystems = self.universe.getSurroundingPlanets(player.location.name)

                        def planetStr(p):
                            return f"{p.name} coords: {p.toStr()} (dist: {p.dist(player.location):.2f})"

                        msg = ""
                        for planet in subsystems:
                            pre = "    "
                            if planet == player.location:
                                pre = " *  "
                            msg += f"{pre}{planetStr(planet)}\n"
                        await message.channel.send(msg)

                    elif args[0] == "system":
                        player = self.players[who]
                        systems = self.universe.getGalaxyWithPlanet(player.location.name).systems

                        def systemStr(s):
                            return f"{s.name} coords: {s.toStr()} (dist: {s.dist(player.location):.2f})"

                        msg = ""
                        for system in systems:
                            pre = "    "
                            msg += f"{pre}{systemStr(system)}\n"
                        await say(msg)

                    elif args[0] == "galaxy":
                        pass
                    else:
                        await message.channel.send(f"Expected argument (planet|system|galaxy) not '{args[0]}'")
            elif cmd == "clear":
                pass
                # messages = await message.channel.history(limit=200).flatten()
                # for msg in messages:
                #     await msg.delete()
            elif cmd == "add":
                ans = reduce(lambda a, b: float(a) + float(b), args)
                await message.channel.send(f'= {ans}')
            else:
                await message.channel.send(f'Umm.. that command literally makes no sense...')

        except ValueError as e:
            await message.channel.send(f'{e}')
