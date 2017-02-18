from random import *
from Critter import Critter

class Specie:
    SPEED_MIN, SPEED_MAX = 0.1, 1.0
    SIZE_MIN, SIZE_MAX = 1, 5
    FOOD_MIN, FOOD_MAX = 0.1, 1
    TURN_SPEED_MIN, TURN_SPEED_MAX = 30, 45
    DETECT_MIN, DETECT_MAX = 1, 5

    def __init__(self, *args, **kwargs):
        self.speed  = 1 # starts as 1 (size per second)
        self.startSize = 1 # starting food
        self.foodDecayRate = .01 # .01 speed
        self.divideSize = 1.5 * self.startSize # 1.5 * start size
        self.turnSpeedVector = 45 # deg / sec (45 / sec)
        self.detectDistance = 2
        self.directionVector = [0,0]
        self.color = "#FF0000"
        self.typeName = "species_name"
        self.individuals = []
        self.birthNumber = 0

    def random_initializer(self):
        self.speed = uniform(Specie.SPEED_MIN, Specie.SPEED_MAX)
        self.startSize = uniform(Specie.SPEED_MIN, Specie.SPEED_MAX)
        self.foodDecayRate = uniform(Specie.FOOD_MIN, Specie.FOOD_MAX)
        self.divideSize = 1.5 * self.startSize
        self.turnSpeedVector = uniform(Specie.TURN_SPEED_MIN, Specie.TURN_SPEED_MAX)
        self.detectDistance = uniform(Specie.DETECT_MIN, Specie.DETECT_MAX)
        r = lambda: random.randint(0, 255)
        self.color = '#%02X%02X%02X' % (r(),r(),r())
        self.build_pop()

    #fucntion that builds a list
    def build_pop(self):
        '''
        this function fills the member population with a seed gen of x Critters
        :return: void
        '''
        for i in range(0, self.individuals):
            this_critter = Critter()
            self.individuals[0] = this_critter

    #class variable that builds population
    #birth new members based on div size
    def determine_birth(self):
        for i in self.individuals:
            pass
    #remove dead members

    def decide_fate(self):
        pass