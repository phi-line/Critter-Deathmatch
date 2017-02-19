import math
from random import randint

class Critter:
    def __init__(self, *args,**kwargs):
        self.foodAmount = kwargs.pop('foodAmount', 1000)                      #starting health
        self.size = kwargs.pop('size',self.foodAmount/100)   #diameter in pixels
        self.foodDecayRate = kwargs.pop('foodDecayRate', 10)       #10 #food lost per second
        self.divideSize = kwargs.pop('divideSize',self.size * 1.5)    # having greater than this amount triggers a division
        self.turnSpeedVector = kwargs.pop('turnSpeedVector', 90)         #45  # amount the heading can change a second in deg / sec (45 / sec)
        self.detectDistance = kwargs.pop('detectDistance', 3)          #2 # number of radii beyond this radius that this can "see"
        self.heading = kwargs.pop('heading',0)                            # direction of travel in degrees
        self.location = kwargs.pop('location',[300, 300]) #[300,300] # pixel coordinates
        self.color = kwargs.pop('color',"#00FF00")                      #"#00FF00" # display color
        self.name = kwargs.pop('name', 0)                      #0 # birth id given from specie.py
        self.speed = kwargs.pop('speed',2)                   #1 # number of radii per second this can travel in a straight line
        self.alive = kwargs.pop('alive',True)
        self.typeName = kwargs.pop('typeName',0)                  #0 # the name of the species, is a number representing the index position in the species array, given by species.py
        self.touching = kwargs.pop('touching',False)                       # touching another object.
        self.needs_update = kwargs.pop('needs_update',True)                   # needs to be updated because its to old, to big, in combat
        self.whoTouching = kwargs.pop('whoTouching',[])                       # a 2 element list of the species id and individual id of whomever this is touching
        self.gen = kwargs.pop('gen',0)                        #0 # what generation this is

    def decide_action(self, species, foods):
        '''
        decide action based on knowledge of species and food
        :param speciesLst: list of species
        :param foodLst: list of food
        :return: none
        '''
        # self.heading = 0 # to the left for demo
        shifts = []
        shiftSum = 0

        theta_1 = 0.0
        imperative_1 = 0
        scaleFactor = 0

        for specie in species:
            for individual in specie.individuals:
                if (individual.alive and self.scale(individual) <= 1):
                    theta_1 = 0.0
                    imperative_1 = 0
                    scaleFactor = self.scale(individual)

                    if (individual.typeName == self.typeName):
                        theta_1 = self.case_4(individual)
                        imperative_1 = 2
                    elif(individual.typeName != self.typeName):
                        if(individual.size > self.size):
                            theta_1 = self.case_1(individual)
                            imperative_1 = 5
                        else:
                            theta_1 = self.case_3(individual)
                            imperative_1 = 3

                newShift = theta_1 * imperative_1 * scaleFactor
                shifts.append(newShift)

        for food in foods:
            if (food.alive and self.scale(food) <= 1):
                theta_2 = self.case_2(food)
                imperative_2 = 4
                scale_2 = self.scale(food) + 0#1000/(self.foodAmount*500)
                newShift_2 = theta_2 * imperative_2 * scale_2
                shifts.append(newShift_2)
                break

        wiggle = self.case_5()
        shifts.append(wiggle)

        for value in shifts:
            shiftSum += value
        shift = int(self.turnSpeedVector * shiftSum / (len(shifts)*2))
        shift = shift % 360
        #print(shift)
        '''
        if (shift > self.turnSpeedVector):
            shift = self.turnSpeedVector
        if (shift < -1*self.turnSpeedVector):
            shift = -1*self.turnSpeedVector
        '''
        # edge detection
        print(self.heading,'\t',shift)
        self.heading = self.heading + shift
        #print(self.heading)

    def scale(self, other):
        '''
        dist between self and other
        :param other:
        :return:
        '''
        distSquared = (other.location[0] - self.location[0])**2 + (other.location[1] - self.location[1])**2
        dist = math.sqrt(distSquared)
        if (dist == 0):
            dist = self.detectDistance-0.01
        scale = (self.size + self.detectDistance*self.size) / dist
        return scale

    def case_1(self, other):
        '''
        run from bad guy
        :param other:
        :return:
        '''
        y = (other.location[1] - self.location[1])
        x = (other.location[0] - self.location[0])

        if (x != 0):
            y_over_x = y / x
            targetTheta = math.tan(y_over_x)

        if (y < 0):
            targetTheta = 270
        else:
            targetTheta = 90

        theta = 180 + (targetTheta - self.heading)

        return theta

    def case_2(self, food):
        '''
        chase down food
        :param food:
        :return:
        '''
        y = (food.location[1] - self.location[1])
        x = (food.location[0] - self.location[0])

        if(x != 0):
            y_over_x = y / x
            targetTheta = math.tan(y_over_x)

        if(y < 0):
            targetTheta = 270
        else:
            targetTheta = 90

        theta = 0 + (targetTheta - self.heading)

        return theta

    def case_3(self,other):
        '''
        chase down tiny bad guy
        :param other:
        :return:
        '''
        y = (other.location[1] - self.location[1])
        x = (other.location[0] - self.location[0])

        if (x != 0):
            y_over_x = y / x
            targetTheta = math.tan(y_over_x)

        if (y < 0):
            targetTheta = 270
        else:
            targetTheta = 90

        theta = 0 + (targetTheta - self.heading)

        return theta

    def case_4(self, other):
        '''
        follow friend
        :param other:
        :return:
        '''
        theta = 0 + (other.heading - self.heading)

        return theta

    def case_5(self):
        '''
        wiggle
        :return:
        '''
        theta = 0 #randint(0, 2) - 1
        return theta

    #include case 6: going out of bounds

    def move(self, frameTime):
        '''
        replace current location with new one
        :param newLocation: list of x,y
        :return: none
        '''
        correctTheta = self.heading % 360
        theta = (correctTheta * 2 * math.pi) / 360
        self.location[0] = self.location[0] + (frameTime * self.speed * self.size) * math.cos(theta)
        self.location[1] = self.location[1] - (frameTime * self.speed * self.size) * math.sin(theta)

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
        pass

    def update(self, speciesLst, foodLst):
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
                        individual.alive = False # eating target
                        self.size += individual.size
                        self.foodAmount += individual.foodAmount
                    elif(self.size < individual.size):
                        self.alive = False # being ate by target
                        individual.size += self.size
                        individual.foodAmount += self.foodAmount
                    else:
                        pass
        for food in foodLst:
            # check if collided with food
            if( Critter.is_collided(self.location, food.location,
                                    self.size, food.size) and
                food.alive):
                #print("Hit food")
                self.needs_update = True
                self.foodAmount += food.consume()

        self.speed = 20 / self.size

