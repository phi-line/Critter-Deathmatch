from random import randint, uniform, random, randrange, choice
from Critter import Critter
from math import *

class Specie:
    SPEED_MIN, SPEED_MAX = 0.1, 1.0
    SIZE_MIN, SIZE_MAX = 1, 5
    FOOD_MIN, FOOD_MAX = 0.1, 1
    TURN_SPEED_MIN, TURN_SPEED_MAX = 30, 45
    DETECT_MIN, DETECT_MAX = 1, 5
    SCALAR_MIN, SCALAR_MAX = 0.5, 1.5

    def __init__(self, *args, **kwargs):
        self.speed  = kwargs.pop('speed', 1) # starts as 1 (size per second)
        self.startSize = kwargs.pop('startSize', 1) # starting food
        self.foodDecayRate = kwargs.pop('foodDecayRate', .01) # .01 speed
        self.divideSize = kwargs.pop('divideSize', 2 * self.startSize) # 1.5 * start size
        #self.turnSpeedVector = kwargs.pop('turnSpeedVector', 45) # deg / sec (45 / sec)
        self.detectDistance = kwargs.pop('detectDistance', 2)
        #self.directionVector = kwargs.pop('directionVector', 0)
        self.color = kwargs.pop('color', "#FF0000")
        self.typeName = kwargs.pop('typeName', 0)
        self.individuals = kwargs.pop('individuals', [])
        self.birthNumber = kwargs.pop('birthNumber', 0)
        self.startingPopulation = kwargs.pop('startingPopulation', 2)
        self.flee_scalar = kwargs.pop('flee_scalar', 1.5)
        self.food_scalar = kwargs.pop('food_scalar', 1.3)
        self.hunt_scalar = kwargs.pop('hunt_scalar', 1.0)
        self.flock_scalar = kwargs.pop('flock_scalar', 1.0)
        self.frame_time = kwargs.pop('frame_time', 0.02)
        self.world_space = kwargs.pop('world_space',[0,0,1200,600])
        self.random_initializer()

    def random_initializer(self):
        self.speed = uniform(Specie.SPEED_MIN, Specie.SPEED_MAX)
        self.startSize = 1#uniform(Specie.SPEED_MIN, Specie.SPEED_MAX)
        self.foodDecayRate = uniform(Specie.FOOD_MIN, Specie.FOOD_MAX)
        self.divideSize = 2.0 * self.startSize
        #self.turnSpeedVector = uniform(Specie.TURN_SPEED_MIN, Specie.TURN_SPEED_MAX)
        self.detectDistance = uniform(Specie.DETECT_MIN, Specie.DETECT_MAX)
        #self.directionVector = 0 #Specie.angle_to_vector(uniform(0,360))
        self.color = Specie.gen_hex_colour_code()
        self.flee_scalar = uniform(Specie.SCALAR_MIN, Specie.SCALAR_MAX)
        self.food_scalar = uniform(Specie.SCALAR_MIN, Specie.SCALAR_MAX)
        self.hunt_scalar = uniform(Specie.SCALAR_MIN, Specie.SCALAR_MAX)
        self.flock_scalar = uniform(Specie.SCALAR_MIN, Specie.SCALAR_MAX)

        self.build_pop()

    @staticmethod
    def angle_to_vector(angle):
        return [int(cos(pi)),-int(sin(pi))]

    @staticmethod
    def gen_hex_colour_code():
        return "#" + ''.join([choice('0123456789ABCDEF') for x in range(6)])
        #+ str(hex(randint(0, 16777215))[2:].upper

    def gen_hue_DNA(self):
        '''
        generates a hue depending on the scalar values set in the critter constructor
        R - hunt_scalar / 2
        G - food_scalar / 2
        B - flee_scalar / 2
        :return: list(color) as HEX
        '''
        R = (self.hunt_scalar / 2.0)
        G = (self.food_scalar / 2.0)
        B = (self.flee_scalar / 2.0)
        color = self.rgb_to_hex(int(R*255), int(G*255), int(B*255))
        return color

    @staticmethod
    def rgb_to_hex(r,g,b):
        return '#%02x%02x%02x' % (r,g,b)

    #fucntion that builds a list
    def build_pop(self):
        '''
        this function fills the member population with a seed gen of x Critters
        :return: void
        '''
        for i in range(0, self.startingPopulation):
            this_critter = Critter( location=[randint(50,1150),randint(50,550)],
                                   heading=0,
                                    name=i,
                                    foodAmount=1500,
                                    typeName=self.typeName,
                                    speed=7,
                                    startSpeed=1,
                                    foodDecayRate=0.1,
                                    color=self.gen_hue_DNA(),
                                    flee_scalar=self.flee_scalar,
                                    food_scalar=self.food_scalar,
                                    hunt_scalar=self.hunt_scalar,
                                    flock_scalar=self.flock_scalar,
                                    frame_time=self.frame_time,
                                    world_x_min=self.world_space[0],
                                    world_y_min=self.world_space[1],
                                    world_x_max=self.world_space[2],
                                    world_y_max=self.world_space[3])
            #print(this_critter.location[0],'\t',this_critter.location[1])
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
                dir = 90#randrange(0, 180)
                new_x = i.location[0]
                new_y = i.location[1]
                childA = Critter(foodAmount=(i.foodAmount/2.2),
                                 #size=(i.size/2),
                                 location=[new_x-randint(15,45),new_y-randint(15,45)],
                                 heading=dir,
                                 color=i.color,
                                 speed=9,#i.speed,
                                 typeName=self.typeName,
                                 name=len(self.individuals) + 1,
                                 frame_time=self.frame_time,
                                 world_x_min=self.world_space[0],
                                 world_y_min=self.world_space[1],
                                 world_x_max=self.world_space[2],
                                 world_y_max=self.world_space[3])
                muDir = 270#randrange(180, 360)
                childB = Critter(foodAmount=(i.foodAmount/2.2),
                                 #size=(i.size/2),
                                 location=[new_x+randint(15,45),new_y+randint(15,45)],
                                 heading=muDir,
                                 color=i.color,
                                 speed=9,#i.speed,
                                 typeName=self.typeName,
                                 name=len(self.individuals) + 1,
                                 frame_time=self.frame_time,
                                 world_x_min=self.world_space[0],
                                 world_y_min=self.world_space[1],
                                 world_x_max=self.world_space[2],
                                 world_y_max=self.world_space[3])
                i.alive = False
                self.individuals.remove(i)
                self.individuals.append(childA)
                self.individuals.append(childB)

    #remove dead members
    def decide_fate(self):
        '''
        Removed dead flagged members from the population
        :return: void
        '''
        for i in self.individuals:
            if not i.alive:
                self.individuals.remove(i)