from random import *

class Specie:
    SIZE_MIN = 0.1
    SIZE_MAX = 1.0
    SPEED_MIN = 0.1
    SPEED_MAX = 1.0

    def __init__(self, *args, **kwargs):

        self.speed  = 1 # starts as 1 (size per second)
        self.startSize = 1 # starting food
        self.foodDecayRate = .01 # .01 speed
        self.divideSize = 1.5 * self.startSize # 1.5 * start size
        self.turnSpeedVector = 45 # deg / sec (45 / sec)
        self.detectDistance = self.startSize + (2 * self.startSize)
        self.directionVector = [0,0]
        self.color = "#FF0000"
        self.typeName = "species_name"
        self.individuals = 10
        self.birthNumber = 0

    def random_initializer(self):
        self.speed = uniform(0.5 1.5)
        self.startSize = uniform(1, 5)
        self.foodDecayRate = uniform(0.1, 1)
        self.divideSize = uniform(, Specie.SIZE_MAX)
        self.turnSpeedVector = uniform(Specie.SIZE_MIN, Specie.SIZE_MAX)
        self.detectDistance = uniform(Specie.SIZE_MIN, Specie.SIZE_MAX)
        self.directionVector = uniform(Specie.SIZE_MIN, Specie.SIZE_MAX)
        self.color = "#FF0000"
        self.typeName = uniform(Specie.SIZE_MIN, Specie.SIZE_MAX)
        self.individuals = uniform(Specie.SIZE_MIN, Specie.SIZE_MAX)
        self.birthNumber = 0
