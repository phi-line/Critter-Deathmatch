import math
from random import randint
from colorsys import hsv_to_rgb, rgb_to_hsv

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
        self.birthFoodAmount = kwargs.pop('foodAmount', 1000)
        # list of indexes for nearest objects:
        # large,food,small,friend
        self.nearest = []
        self.mostImperativeIndex = 0
        self.nearest_empty = True
        self.newLocation = [0,0]
        self.prevHeading = 0
        self.target = [0,0]

        self.frame_time = kwargs.pop('frame_time', 0.02)

    def distance(self, other):
        distSquared = (other.location[0] - self.location[0]) ** 2 + (other.location[1] - self.location[1]) ** 2
        dist = math.sqrt(distSquared)
        return dist

    def init_nearest(self,species,foods):
        if not self.nearest_empty:
            return

        self.nearest.append(Critter())
        self.nearest.append(Critter())
        self.nearest.append(Critter())
        self.nearest.append(Critter())

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
        if (new < cur or not self.nearest[0].alive):
            self.nearest[0] = other

    def compare_near_food(self, other):
        cur = self.distance(self.nearest[1])
        new = self.distance(other)
        if (new < cur or not self.nearest[1].alive):
            #print('new target: ', other.name,' dist: ', new)
            self.nearest[1] = other

    def compare_near_small(self, other):
        cur = self.distance(self.nearest[2])
        new = self.distance(other)
        if (new < cur or not self.nearest[2].alive):
            self.nearest[2] = other

    def compare_near_friend(self, other):
        cur = self.distance(self.nearest[3])
        new = self.distance(other)
        if (new < cur or not self.nearest[3].alive):
            self.nearest[3] = other

    #method to find most imperative index
    def update_imperative(self):
        if self.size <= 0:
            return

        large = -1
        food = -1
        small = -1
        friend = -1

        largeMod = self.flee_scalar    #flee
        foodMod = self.food_scalar     #food
        smallMod = self.hunt_scalar    #hunt
        friendMod = self.flock_scalar  #flock

        self.mostImperativeIndex = -1

        if self.nearest[0].alive:
            large   = 1.0 - (self.distance(self.nearest[0])/(self.detectDistance*self.size))
            large   *= largeMod

        if self.nearest[1].alive:
            #print(self.distance(self.nearest[1]))
            food    = 1.0 - (self.distance(self.nearest[1])/(self.detectDistance*self.size))
            food    *= abs(1.0 - (self.foodAmount/(self.birthFoodAmount*self.divideSize)))
            food    *= foodMod

        if self.nearest[2].alive:
            small   = 1.0 - (self.distance(self.nearest[2])/(self.detectDistance*self.size))
            small   *= smallMod

        if self.nearest[3].alive:
            friend  = 1.0 - (self.distance(self.nearest[3])/(self.detectDistance*self.size))
            friend  *= friendMod

        #print('name: ',self.typeName,',',self.name,'\t',large,'\t',food,'\t',small,'\t',friend)

        #find the largest value from above
        if(large > 0 and large > food and large > small and large > friend):
            self.mostImperativeIndex = 0
        elif(food > 0 and food > large and food > small and food > friend):
            self.mostImperativeIndex = 1
        elif(small > 0 and small > large and small > food and small > friend):
            self.mostImperativeIndex = 2
        elif( friend > 0 and friend > large and friend > food and friend > small):
            self.mostImperativeIndex = 3
        else:
            self.mostImperativeIndex = self.mostImperativeIndex

        if(self.mostImperativeIndex >=0):
            if self.nearest[self.mostImperativeIndex].size == self.size:
                self.mostImperativeIndex = 1

            if self.nearest[self.mostImperativeIndex].typeName == self.typeName:
                if self.nearest[self.mostImperativeIndex].name != self.name:
                    self.mostImperativeIndex = 3

            if not self.nearest[self.mostImperativeIndex].alive:
                self.mostImperativeIndex = 1
            #print('start target:  ', self.location)
            self.target = self.nearest[self.mostImperativeIndex].location
            #self.target[0] = self.nearest[self.mostImperativeIndex].location[0]
            #self.target[1] = self.nearest[self.mostImperativeIndex].location[1]
            #print('  end target:  ', self.location)
        else:
            self.mostImperativeIndex = -1

        #print(self.mostImperativeIndex)

    def point_away_from_large(self):
        #print('point_away_from_large')
        x = -1 * int(self.nearest[0].location[0] - self.location[0])
        y = int(self.nearest[0].location[1] - self.location[1])

        if (x == 0):
            if (y < 0):
                # print("y<0")
                targetTheta = 270
            else:
                # print("y>0")
                targetTheta = 90
        else:
            ratio = y / x
            targetTheta = math.atan(ratio)
            targetTheta = int((targetTheta * 180) / math.pi)

        # print(x,'\t',y)
        # print(targetTheta)
        if (x < 0):
            targetTheta = targetTheta + 180

        if (targetTheta < 0):
            targetTheta = targetTheta + 360
        # print(targetTheta)
        # print('frame end\n')
        #self.speed +=0.1
        if self.speed > 12:
            self.speed = 12
        self.heading = targetTheta - self.heading / randint(180, 360)

    def point_at_food(self):
        #print('name: ',self.nearest[1].name)
        x = int(self.nearest[1].location[0] - self.location[0])
        y = -1 * int(self.nearest[1].location[1] - self.location[1])

        if (x == 0):
            if (y < 0):
                #print("y<0")
                targetTheta = 270
            else:
                #print("y>0")
                targetTheta = 90
            return
        else:
            ratio = y / x
            targetTheta = math.atan(ratio)
            targetTheta = int((targetTheta * 180) / math.pi)

        #print(self.heading,'\t',x,'\t',y)
        #print(targetTheta)
        if (x < 0):
            targetTheta = targetTheta + 180

        if (targetTheta < 0):
            targetTheta = targetTheta + 360
        #print(targetTheta)
        #print('frame end\n')

        self.heading = targetTheta
        #print(self.name,'\t',x, ' \t', y,'\t',self.heading)

    def point_at_small(self):
        #print('point_at_small')
        if self.size > self.nearest[2].size:
            self.point_at_food()
            return
        x = int(self.nearest[2].location[0] - self.location[0])
        y = -1 * int(self.nearest[2].location[1] - self.location[1])

        if (x == 0):
            if (y < 0):
                # print("y<0")
                targetTheta = 270
            else:
                # print("y>0")
                targetTheta = 90
        else:
            ratio = y / x
            targetTheta = math.atan(ratio)
            targetTheta = int((targetTheta * 180) / math.pi)

        # print(x,'\t',y)
        # print(targetTheta)
        if (x < 0):
            targetTheta = targetTheta + 180

        if (targetTheta < 0):
            targetTheta = targetTheta + 360
        # print(targetTheta)
        # print('frame end\n')

        self.heading = targetTheta

    def point_with_friend(self):
        #print('point_with_friend')
        x = int(self.nearest[3].location[0] - self.location[0])
        y = -1*int(self.nearest[3].location[1] - self.location[1])

        if (x == 0):
            if (y < 0):
                # print("y<0")
                targetTheta = 270
            else:
                # print("y>0")
                targetTheta = 90
        else:
            ratio = y / x
            targetTheta = math.atan(ratio)
            targetTheta = int((targetTheta * 180) / math.pi)

        # print(x,'\t',y)
        # print(targetTheta)
        if (x < 0):
            targetTheta = targetTheta + 180

        if (targetTheta < 0):
            targetTheta = targetTheta + 360
        # print(targetTheta)
        # print('frame end\n')

        self.heading = targetTheta#self.heading - targetTheta/randint(36,72)

    def point_heading(self):
        if self.mostImperativeIndex == 0:
            self.point_away_from_large()
        elif self.mostImperativeIndex == 1:
            self.point_at_food()
        elif self.mostImperativeIndex == 2:
            self.point_at_small()
        elif self.mostImperativeIndex == 3:
            self.point_with_friend()
        else:
            #print('critter[',self.name,'] has no target')
            self.target = self.location
            self.heading += (randint(0,30) - 15)

    def decide_action(self, species, foods):
        '''
        decide action based on knowledge of species and food
        :param speciesLst: list of species
        :param foodLst: list of food
        :return: none
        '''
        #print('start action:     ',self.location)
        if self.nearest_empty:
            self.init_nearest(species,foods)

        for food in foods.foodLst:
            self.compare_near_food(food)

        for specie in species:
            for individual in specie.individuals:
                if individual.alive:
                    if (individual.typeName == self.typeName and individual.name != self.name):
                        self.compare_near_friend(individual)
                    else:
                        if individual.size > self.size:
                            self.compare_near_large(individual)
                        elif individual.size < self.size:
                            self.compare_near_small(individual)
        #print('start imperative: ', self.location)
        self.update_imperative()
        #print('  end imperative: ', self.location)

        self.point_heading()
        #print('  end action:     ', self.location)


        #print(self.heading,' \t',self.location[0],'\t',self.location[1],'\t',self.mostImperativeIndex)

        #self.heading = 0 # to the left for demo

    def move(self, frameTime):


        if self.location[0] + self.size > 1195:
            # perform vector reflection from vector2.right
            self.heading = randint(110, 150)  # self.vector_reflect([-1, 0])
        elif self.location[0] - self.size < 5:
            # perform vector reflection from vector2.left
            self.heading = randint(0, 20)  # self.vector_reflect([1, 0])
        elif self.location[1] + self.size > 595:
            # perform vector reflection from vector2.down
            self.heading = randint(20, 160)  # self.vector_reflect([0, -1])
        elif self.location[1] - self.size < 5:
            # perform vector reflection from vector2.up
            self.heading = randint(200, 340)  # self.vector_reflect([0, 1])

        antiHeading = (self.heading + 180) % 360
        newHeadingOffset = (abs(antiHeading - self.prevHeading)) % 360
        dampening = (newHeadingOffset / 180)
        if dampening > 1:
            dampening = 1
        #print(dampening)

        correctTheta = self.heading % 360
        theta = (correctTheta * 2 * math.pi) / 360

        self.location[0] = int(self.location[0] + (frameTime * self.speed * self.size * dampening) * math.cos(theta))
        self.location[1] = int(self.location[1] - (frameTime * self.speed * self.size * dampening) * math.sin(theta))

        #print(self.location[0],'\t',self.location[1])

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

        if self.foodAmount <= self.birthFoodAmount*.25:
            self.alive = False

    def update(self,frameTime, speciesLst, foodLst):
        '''
        update status of critter itself
        :param speciesLst: list of species
        :param foodLst: list of food
        :return: none
        '''
        for species in speciesLst:
            for individual in species.individuals:
                # check if collided with target
                if( Critter.is_collided(self.location, individual.location,
                                        self.size, individual.size) and
                    self.typeName != individual.typeName and
                    self.alive and individual.alive):

                    if(self.size > individual.size):
                        # apply damage once from the larger to smaller and then smaller to larger
                        self.apply_damage(individual)
                        pass
                if (self.health <= 0):
                    self.alive = False

                    # if(self.size > individual.size):
                    #     individual.alive = False # eating target
                    #     self.foodAmount += individual.foodAmount
                    # elif(self.size < individual.size):
                    #     self.alive = False # being ate by target
                    #     #individual.foodAmount += self.foodAmount
                    # else:
                    #     pass

        for food in foodLst.foodLst:
            # check if collided with food
            if( Critter.is_collided(self.location, food.location,
                                    self.size, food.size) and
                food.alive):
                #print("Hit food")
                self.needs_update = True
                self.foodAmount += food.consume()
                #foodLst.remove(food)

        self.size = self.foodAmount / self.scaleModifier

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
            rgb[i] = (self.health/100)*255
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