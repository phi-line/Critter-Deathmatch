import math
from random import randint
import Food

class Critter:
    def __init__(self, *args,**kwargs):
        self.scaleModifier = 100
        self.flee_scalar = kwargs.pop('flee_scalar', 1.5)
        self.food_scalar = kwargs.pop('food_scalar', 1.3)
        self.hunt_scalar = kwargs.pop('hunt_scalar', 1.0)
        self.flock_scalar = kwargs.pop('flock_scalar', 1.0)

        self.foodAmount = kwargs.pop('foodAmount', 1500)                      #starting health
        self.health = kwargs.pop('health', int((2*self.foodAmount)/self.scaleModifier))
        self.DPS = kwargs.pop('DPS', int(self.health*self.hunt_scalar))

        self.size = kwargs.pop('size',self.foodAmount/self.scaleModifier)   #diameter in pixels
        self.foodDecayRate = kwargs.pop('foodDecayRate', 0)       #10 #food lost per second
        self.divideSize = kwargs.pop('divideSize',self.size * 2)    # having greater than this amount triggers a division
        #self.turnSpeedVector = kwargs.pop('turnSpeedVector', 30)         #45  # amount the heading can change a second in deg / sec (45 / sec)
        self.detectDistance = kwargs.pop('detectDistance', 5)          #2 # number of radii beyond this radius that this can "see"
        self.heading = kwargs.pop('heading',0)                            # direction of travel in degrees
        self.location = kwargs.pop('location',[0, 0]) #[300,300] # pixel coordinates
        self.color = kwargs.pop('color',"#00FF00")                      #"#00FF00" # display color
        self.name = kwargs.pop('name', 0)                      #0 # birth id given from specie.py
        self.speed = kwargs.pop('speed',1)                   #1 # number of radii per second this can travel in a straight line
        self.startSpeed = kwargs.pop('speed',1)
        self.alive = kwargs.pop('alive',True)
        self.typeName = kwargs.pop('typeName',0)                  #0 # the name of the species, is a number representing the index position in the species array, given by species.py
        self.touching = kwargs.pop('touching',False)                       # touching another object.
        self.needs_update = kwargs.pop('needs_update',True)                   # needs to be updated because its to old, to big, in combat
        self.whoTouching = kwargs.pop('whoTouching',[])                       # a 2 element list of the species id and individual id of whomever this is touching
        self.gen = kwargs.pop('gen',0)                        #0 # what generation this is
        self.birthFoodAmount = kwargs.pop('foodAmount', 1500)
        # list of indexes for nearest objects:
        # large,food,small,friend
        self.nearest = []
        self.mostImperativeIndex = 0
        self.nearest_empty = True
        self.newLocation = [0,0]
        self.prevHeading = 0
        self.target = [0,0]

        self.frame_time = kwargs.pop('frame_time', 0.02)

        self.world_x_min = kwargs.pop('world_x_min',0)
        self.world_y_min = kwargs.pop('world_y_min',0)
        self.world_x_max = kwargs.pop('world_x_max',1200)
        self.world_y_max = kwargs.pop('world_y_max',600)

    def distance(self, other):
        distSquared = (other.location[0] - self.location[0]) ** 2 + (other.location[1] - self.location[1]) ** 2
        dist = math.sqrt(distSquared)
        return dist

    def init_nearest(self,species,foods):
        if not self.nearest_empty:
            return

        self.nearest.append(self)
        self.nearest.append(self)
        self.nearest.append(self)
        self.nearest.append(self)

        if(len(foods.foodLst) != 0):
            self.nearest[1] = foods.foodLst[0]

        spacesFilled = 1

        for specie in species:
            if spacesFilled >= 4:
                break
            for individual in specie.individuals:
                if spacesFilled >= 4:
                    break
                if(individual.typeName == self.typeName and individual.name != self.name):
                    self.nearest[3] = individual
                    spacesFilled += 1
                elif(individual.typeName != self.typeName):
                    self.nearest[0] = individual
                    self.nearest[2] = individual
                    spacesFilled += 2

        self.nearest_empty = False


    def compare_near_large(self,other):
        cur = self.distance(self.nearest[0])
        new = self.distance(other)
        if (new < cur or not self.nearest[0].alive or self.nearest[0].name == self.name):
            self.nearest[0] = other

    def compare_near_food(self, other):
        cur = self.distance(self.nearest[1])
        new = self.distance(other)
        if (new < cur or not self.nearest[1].alive or self.nearest[1].name == self.name):
            #print('new target: ', other.name,' dist: ', new)
            self.nearest[1] = other

    def compare_near_small(self, other):
        cur = self.distance(self.nearest[2])
        new = self.distance(other)
        if (new < cur or not self.nearest[2].alive or self.nearest[2].name == self.name):
            self.nearest[2] = other

    def compare_near_friend(self, other):
        cur = self.distance(self.nearest[3])
        new = self.distance(other)
        if (new < cur or not self.nearest[3].alive or self.nearest[3].name == self.name):
            self.nearest[3] = other

    def move(self):
        if self.location[0] + self.size > self.world_x_max*0.95:
            self.heading = randint(110, 250)
        elif self.location[0] - self.size < self.world_x_min*0.95:
            self.heading = randint(110, 250) + 180
        elif self.location[1] + self.size > self.world_y_max*0.95:
            self.heading = randint(20, 160)
        elif self.location[1] - self.size < self.world_y_min*0.95:
            self.heading = randint(200, 340)

        antiHeading = (self.heading + 180) % 360
        newHeadingOffset = (abs(antiHeading - self.prevHeading)) % 360
        dampening = (newHeadingOffset / 180)
        if dampening > 1:
            dampening = 1

        correctTheta = self.heading % 360
        theta = (correctTheta * 2 * math.pi) / 360

        self.location[0] = int(self.location[0] + (self.frame_time * self.speed * self.size * dampening) * math.cos(theta))
        self.location[1] = int(self.location[1] - (self.frame_time * self.speed * self.size * dampening) * math.sin(theta))

        self.prevHeading = self.heading

    @staticmethod
    def is_collided(fLocationLst, sLocationLst, fRadiusFlt, sRadiusFlt):
        '''
        check whether collided
        :param fLocationLst: first list of x,y
        :param sLocationLst: second list of x,y
        :param fRadiusFlt: float of radius
        :param sRadiusFlt: float of radius
        :return: boolean
        '''
        xCal = ( fLocationLst[0] - sLocationLst[0] ) ** 2
        yCal = ( fLocationLst[1] - sLocationLst[1] ) ** 2
        rCal = ( fRadiusFlt + sRadiusFlt ) ** 2
        return (xCal + yCal) <= rCal

    def check_state(self,species,foods):
        '''
        checks if this individual is in collision with another individual or food
        occurs after the move function
        may set touching to true
            get id of person im touching
        sets need_update to true
        :param species:
        :param foods:
        :return:
        '''
        self.foodAmount -= self.foodDecayRate
        self.size = (self.foodAmount) / self.scaleModifier
        #self.speed = self.startSpeed * (self.birthFoodAmount / (self.foodAmount))

        if (self.foodAmount <= self.birthFoodAmount*.25 or self.health <= 0):
            self.alive = False

    def update(self, speciesLst, foodLst):
        '''
        update status of critter itself
        :param speciesLst: list of species
        :param foodLst: list of food
        :return: none
        '''
        large = self.nearest[0]
        food = self.nearest[1]
        small = self.nearest[2]
        friend = self.nearest[3]

        if (Critter.is_collided(self.location, large.location,self.size, large.size) and self.typeName != large.typeName and self.alive and large.alive):
            if (self.size > large.size):
                self.apply_damage(large)

        elif(Critter.is_collided(self.location, food.location,self.size, food.size) and food.alive and (food != self)):
            self.needs_update = True
            self.foodAmount += food.consume()

        elif (Critter.is_collided(self.location, small.location,self.size, small.size) and self.typeName != small.typeName and self.alive and small.alive):
            if (self.size > small.size):
                self.apply_damage(small)

        elif (Critter.is_collided(self.location, friend.location,self.size, friend.size) and self.typeName != friend.typeName and self.alive and friend.alive):
            if (self.size > friend.size):
                self.apply_damage(friend)

    def apply_damage(self, other):
        self.DPS = int(self.health*self.hunt_scalar*10)
        other.DPS = int(other.health*other.hunt_scalar*10)
        # print(other.DPS, self.health)
        self.health -= float(other.DPS)*self.frame_time
        other.health -= float(self.DPS)*self.frame_time
        self.update_color()
        other.update_color()
        # print(other.DPS, self.health)
        # print ("\n")

    def update_color(self):
        rgb = self.hex_to_rgb(self.color)
        rgb = list(rgb)
        for i in range(0, len(rgb)):
            rgb[i] *= (self.health/int((2*self.birthFoodAmount)/self.scaleModifier))
            rgb[i] = int(rgb[i])
            if rgb[i] >= 255:
                rgb[i] = 255
            if rgb[i] <= 0:
                rgb[i] = 0
        self.color = self.rgb_to_hex(rgb[0],rgb[1],rgb[2])

    @staticmethod
    def rgb_to_hex(r,g,b):
        return '#%02x%02x%02x' % (r,g,b)

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))