import math

class Critter:
    def __init__(self, params, *args,**kwargs):
        self.foodAmount = 1000                      #starting health
        self.size = self.foodAmount/100             #diameter in pixels
        self.foodDecayRate = params[0]              #10 #food lost per second
        self.divideSize = self.size * params[1]     # having greater than this amount triggers a division
        self.turnSpeedVector = params[2]            #45  # amount the heading can change a second in deg / sec (45 / sec)
        self.detectDistance = params[3]             #2 # number of radii beyond this radius that this can "see"
        self.heading = 0                            # direction of travel in degrees
        self.location = [params[4][0],params[4][1]] #[300,300] # pixel coordinates
        self.color = params[5]                      #"#00FF00" # display color
        self.name = params[6]                       #0 # birth id given from specie.py
        self.speed = params[7]                      #1 # number of radii per second this can travel in a straight line
        self.alive = True
        self.typeName = params[8]                   #0 # the name of the species, is a number representing the index position in the species array, given by species.py
        self.touching = False                       # touching another object.
        self.needs_update = False                   # needs to be updated because its to old, to big, in combat
        self.whoTouching = []                       # a 2 element list of the species id and individual id of whomever this is touching
        self.gen = params[9]                        #0 # what generation this is

    def decide_action(self, species, foods):
        '''
        decide action based on knowledge of species and food
        :param speciesLst: list of species
        :param foodLst: list of food
        :return: none
        '''
        self.heading = 0 # to the left for demo

    def move(self, frameTime):
        '''
        replace current location with new one
        :param newLocation: list of x,y
        :return: none
        '''
        theta = ((self.heading) * 2 * math.pi) / 360
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
                                        self.size, individual.size) ):
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
                food.alive == True):
                self.foodAmount += food.foodAmount # add food amount
                food.alive = False # kill food

