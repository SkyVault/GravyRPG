class Module:
    def __init__(self):
        pass


class SpaceShip:
    def __init__(self, name="Unidentified Space Vessel", descr="None"):
        self.modules = []
        self.baseSpeed = 0.5
        self.name = name
        self.descr = descr

    def info(self):
        return f"Base Speed: {self.baseSpeed} l/y\nModules: {self.modules}"


class AX00SpaceFreighter(SpaceShip):
    def __init__(self):
        super().__init__(
            "AX00 Space Freighter",
            f"A small Freighter ship, slow but reliable... well not really, but it flies\n")
