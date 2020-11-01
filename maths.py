from math import sqrt
from random import random


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other) -> float:
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    @property
    def pos(self):
        return self.x, self.y

    def toStr(self):
        return f"({self.x:.2f} {self.y:.2f})"


def randRange(mn, mx):
    return mn + random() * mx
