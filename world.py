from dataclasses import dataclass
from random import random
from typing import Tuple, List

from maths import Coord, randRange


class Location(Coord):
    def __init__(self, pos: Tuple[float, float] = (0, 0), name="Unknown", descr="Unknown region... you lost boy"):
        super().__init__(*pos)
        self.name = name
        self.descr = descr

        if self.descr == "":
            self.descr = type(self)


class Universe(Location):
    def __init__(self, galaxies=[]):
        # Universe is the center of the universe
        super().__init__((0, 0))
        self.galaxies = galaxies
        for g in self.galaxies:
            gx, gy = g.x, g.y
            for s in g.systems:
                sx, sy = s.x, s.y
                s.x = gx + sx
                s.y = gy + sy
                for p in s.subsystems:
                    px, py = p.x, p.y
                    p.x, p.y = gx + sx + px, gy + sy + py

    def enumerate(self):
        for gal in self.galaxies:
            for system in gal.systems:
                for sub in system.subsystems:
                    yield gal, system, sub

    def getPlanetByName(self, name):
        for (gal, sys, sub) in self.enumerate():
            if type(sub) is Planet and sub.name == name:
                return sub, sys, gal
        return Location(), Location(), Location()

    def getSurroundingPlanets(self, name):
        for gal in self.galaxies:
            for system in gal.systems:
                for sub in system.subsystems:
                    if type(sub) is Planet and sub.name == name:
                        return system.subsystems

    def getGalaxyWithPlanet(self, name):
        for (gal, sys, sub) in self.enumerate():
            if sub.name == name:
                return gal
        return None

    def getSurroundingSystems(self, name):
        for gal in self.galaxies:
            if gal.name == name:
                return gal.systems


class Galaxy(Location):
    def __init__(self, pos, systems=[], name=None, descr=None):
        super().__init__(pos, name, descr)
        self.systems = systems


class System(Location):
    def __init__(self, pos, subsystems=[], name=None, descr=None):
        super().__init__(pos, name, descr)
        self.subsystems = subsystems


class Subsystem(Location):
    def __init__(self, pos, name=None, descr=None):
        super().__init__(pos, name, descr)


class Planet(Subsystem):
    def __init__(self, pos, places=[], name=None, descr=None):
        super().__init__(pos, name, descr)
        self.places = places

        has = False
        for p in self.places:
            if type(p) is SpacePort:
                has = True
        if not has:
            print(f"Warning: planet {name} is missing a space port")


class SpaceStation(Subsystem):
    def __init__(self, pos, name=None, descr=None):
        super().__init__(pos, name, descr)


class Place(Location):
    def __init__(self, pos, things=[], name=None, descr=None):
        super().__init__(pos, name, descr)
        self.things = []


class Building(Place):
    def __init__(self, things=[], name=None, descr=None):
        super().__init__((0, 0), things, name, descr)


class SpacePort(Building):
    def __init__(self, name=None, descr=None):
        super().__init__([], name, descr)


class TradePost(Building):
    def __init__(self, name=None, descr=None):
        super().__init__([], name, descr)


def getGravyGalaxy():
    gal = Galaxy((42000.0, 69000.0), [
        System((randRange(-200.0, 400.0), randRange(-200.0, 400.0)), [
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Murcury", places=[
                SpacePort(name="Crater Launch")
            ]),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Venus", places=[
                SpacePort(name="Port of Valcanus")
            ]),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)),
                   name="Earth",
                   descr="A Green planet with an abundance of blue water, atmosphere primarily made of O2 with a population largly of Ants and Humans",
                   places=[
                       SpacePort(name="Nasa Space Port"),
                       TradePost(name="National Trade Post")
                   ]),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Mars", places=[
                SpacePort(name="Port of Nili Fossae")
            ]),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Jupiter", places=[
                SpacePort(name="Port Ganymede Shadow")
            ]),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Saturn", places=[
                SpacePort(name="Port Saturnus IV")
            ]),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Uranus", places=[
                SpacePort(name="Wrinkled Brown Crater")
            ]),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Neptune", places=[
                SpacePort(name="Porteus Oceanus")
            ]),
        ], name="Solar"),
        System((randRange(-200.0, 400.0), randRange(-200.0, 400.0)), [
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Proxima-Centauri-b"),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Trion-6M7I"),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Onuanus"),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Thonkichi"),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Yignerth"),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Phothonia"),
            Planet((randRange(-20.0, 40.0), randRange(-20.0, 40.0)), name="Xi-Sion-5XWL"),
        ], name="Alpha-Centauri")
    ], name="The-Milky-Way")
    return gal


def getUniverse():
    uni = Universe([
        getGravyGalaxy(),
    ])
    return uni
