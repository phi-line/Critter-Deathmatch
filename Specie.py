from random import randint, uniform, random, randrange
from Critter import Critter
from math import *

class Specie:
    SPEED_MIN, SPEED_MAX = 0.1, 1.0
    SIZE_MIN, SIZE_MAX = 1, 5
    FOOD_MIN, FOOD_MAX = 0.1, 1
    TURN_SPEED_MIN, TURN_SPEED_MAX = 30, 45
    DETECT_MIN, DETECT_MAX = 1, 5

    def __init__(self, *args, **kwargs):
        self.speed  = kwargs.pop('speed', 1) # starts as 1 (size per second)
        self.startSize = kwargs.pop('startSize', 1) # starting food
        self.foodDecayRate = kwargs.pop('foodDecayRate', .01) # .01 speed
        self.divideSize = kwargs.pop('divideSize', 1.5 * self.startSize) # 1.5 * start size
        self.turnSpeedVector = kwargs.pop('turnSpeedVector', 45) # deg / sec (45 / sec)
        self.detectDistance = kwargs.pop('detectDistance', 2)
        self.directionVector = kwargs.pop('directionVector', [0,0])
        self.color = kwargs.pop('color', "#FF0000")
        self.typeName = kwargs.pop('typeName', "species_name")
        self.individuals = kwargs.pop('individuals', [])
        self.birthNumber = kwargs.pop('birthNumber', 0)
        self.startingPopulation = kwargs.pop('startingPopulation', 2)
        self.random_initializer()

    def random_initializer(self):
        self.speed = uniform(Specie.SPEED_MIN, Specie.SPEED_MAX)
        self.startSize = uniform(Specie.SPEED_MIN, Specie.SPEED_MAX)
        self.foodDecayRate = uniform(Specie.FOOD_MIN, Specie.FOOD_MAX)
        self.divideSize = 1.5 * self.startSize
        self.turnSpeedVector = uniform(Specie.TURN_SPEED_MIN, Specie.TURN_SPEED_MAX)
        self.detectDistance = uniform(Specie.DETECT_MIN, Specie.DETECT_MAX)
        self.directionVector = Specie.angle_to_vector(uniform(0,360))
        # r = lambda: random.randint(0, 255)
        self.color = "#000000" # '#%02X%02X%02X' % (r(),r(),r())
        self.build_pop()

    @staticmethod
    def angle_to_vector(angle):
        return [int(cos(pi)),-int(sin(pi))]

    #fucntion that builds a list
    def build_pop(self):
        '''
        this function fills the member population with a seed gen of x Critters
        :return: void
        '''
        for i in range(0, self.startingPopulation):
            this_critter = Critter( location=[randint(0,1200),randint(0,600)],
                                   heading=(randint(0,360)) )
            #print(this_critter.location[0],'\t',this_critter.location[1])
            print(this_critter.heading)
            self.individuals.append(this_critter)

    #class variable that builds population
    #birth new members based on div size
    #food
    def determine_birth(self):
        '''
        determines if an individual is too big and if so it separates
        based on the div size. recalculates food
        :return: void
        '''
        for i in self.individuals:
            if i.size > i.divideSize:
                dir = randrange(0, 360)
                childA = Critter(foodAmount=(i.foodAmount/2),
                                 size=(i.size/2),
                                 location=i.location,
                                 heading=dir)
                muDir = 180 + dir
                if(muDir >= 360):
                    muDir -= 360
                elif(muDir < 0):
                    muDir += 360
                childB = Critter(foodAmount=(i.foodAmount/2),
                                 size=(i.size/2),
                                 location=i.location,
                                 heading=muDir)
                self.individuals.remove(i)
                self.individuals.append(childA)
                self.individuals.append(childB)

    #remove dead members
    def decide_fate(self):
        '''
        Removed dead flagged members from the population
        :return: void
        '''
        for i in self.inividuals:
            if not i.alive:
                self.individuals.remove(i)