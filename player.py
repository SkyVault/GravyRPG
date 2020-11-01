from enum import Enum, auto
from math import atan2, cos, sin
from textwrap import dedent

from maths import Coord
from ship import AX00SpaceFreighter
from world import Planet


class State(Enum):
    GROUNDED = auto()
    TRAVELING = auto()
    ARRIVED = auto()


class Player(Coord):
    def __init__(self, name="Anon"):
        self.location = None
        self.name = name
        self.age = 21

        self.state = State.GROUNDED

        self.credits = 20000

        self.inventory = []
        self.spaceShip = AX00SpaceFreighter()

        self.destination = None
        self.startPos = None
        self.targetMessage = None

    def startTravel(self, dest: Planet, target_message):
        if self.spaceShip is None:
            return
        self.x, self.y = self.location.x, self.location.y
        self.startPos = Coord(self.x, self.y)
        self.destination = dest
        self.state = State.TRAVELING
        self.targetMessage = target_message
        print(self.targetMessage)

    async def updateTargetMessage(self):
        if self.state is not State.TRAVELING:
            return
        if self.targetMessage is not None:
            try:
                perc = int(self.travelPercent / 2)
                fill = int(50 - perc)
                string = ("=" * perc) + ("-" * fill)
                await self.targetMessage.edit(content=f"`traveling to '{self.destination.name}' [{string}]`")
            except Exception as e:
                print(e)
                self.targetMessage = None
                pass

    def tick(self):
        self.age += 0.1

        if self.state is State.TRAVELING:
            angle = atan2(self.destination.y - self.y, self.destination.x - self.x)
            self.x += cos(angle) * self.spaceShip.baseSpeed
            self.y += sin(angle) * self.spaceShip.baseSpeed

            if self.dist(self.destination) < 1.0:
                self.x = self.destination.x
                self.y = self.destination.y
                self.location = self.destination
                self.state = State.GROUNDED

    def locate(self, universe):
        planet, system, galaxy = universe.getPlanetByName(self.location.name)
        localeStr = f"You are on the planet {planet.name}"
        if self.state is State.TRAVELING:
            localeStr = f"You are traveling to {self.destination.name} from {self.location.name}"
            localeStr += f" ({self.travelPercent}%)"
        return dedent(f"""
            {planet.toStr()}\n
            {localeStr} in
            the '{system.name}' system within the '{galaxy.name}' galaxy
        """).replace('\n', ' ')

    def locateLocal(self):
        localeStr = f"You are on the planet {self.location.name}"
        if self.state is State.TRAVELING:
            localeStr = f"You are traveling to {self.destination.name} from {self.location.name}"
            localeStr += f" ({self.travelPercent}%)"
        return localeStr

    @property
    def travelPercent(self):
        startDist = self.startPos.dist(self.destination)
        dist = self.dist(self.destination)
        return 100 - int(100.0 * float(dist / startDist))

    def __str__(self):
        lns = [
            f"name: {self.name}",
            f"age: {self.age}",
            f"location: {self.location.name}"
        ]

        if self.state is State.TRAVELING:
            lns.append(f"Traveling to {self.destination.name} ({self.travelPercent}%)")

        num = 0
        for ln in lns:
            if len(ln) > num:
                num = len(ln)

        res = "+" + "-" * num + "+\n"
        for ln in lns:
            res += "|" + ln + " " * (num - len(ln)) + "|\n"
        res += "+" + "-" * num + "+\n"
        return res

