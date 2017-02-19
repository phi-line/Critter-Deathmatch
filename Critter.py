import math
import random

class Critter:
    def __init__(self, *args,**kwargs):
        self.foodAmount = kwargs.pop('foodAmount', 1000)                      #starting health
        self.size = kwargs.pop('size',self.foodAmount/100)   #diameter in pixels
        self.foodDecayRate = kwargs.pop('foodDecayRate', 10)       #10 #food lost per second
        self.divideSize = kwargs.pop('divideSize',self.size * 1.5)    # having greater than this amount triggers a division
        self.turnSpeedVector = kwargs.pop('turnSpeedVector', 45)         #45  # amount the heading can change a second in deg / sec (45 / sec)
        self.detectDistance = kwargs.pop('detectDistance', 2)          #2 # number of radii beyond this radius that this can "see"
        self.heading = kwargs.pop('heading',0)                            # direction of travel in degrees
        self.location = kwargs.pop('location',[300, 300]) #[300,300] # pixel coordinates
        self.color = kwargs.pop('color',"#00FF00")                      #"#00FF00" # display color
        self.name = kwargs.pop('name', 0)                      #0 # birth id given from specie.py
        self.speed = kwargs.pop('speed',1)                   #1 # number of radii per second this can travel in a straight line
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
        pass

    # def move(self, frameTime):
    #     theta = ((self.heading) * 2 * math.pi) / 360
    #     self.location[0] = self.location[0] + (frameTime * self.speed * self.size) * math.cos(theta)
    #     self.location[1] = self.location[1] - (frameTime * self.speed * self.size) * math.sin(theta)


    def move(self, frameTime):
        if self.location[0] + self.size> 1200:
            # perform vector reflection from vector2.right
            self.heading = random.randint(110,150)#self.vector_reflect([-1, 0])
        elif self.location[0] - self.size< 0:
            # perform vector reflection from vector2.left
            self.heading = random.randint(0,20) #self.vector_reflect([1, 0])
        if self.location[1] + self.size > 600:
            # perform vector reflection from vector2.down
            self.heading = random.randint(20,160) #self.vector_reflect([0, -1])
        elif self.location[1] - self.size < 0:
            # perform vector reflection from vector2.up
            self.heading = random.randint(200,340) #self.vector_reflect([0, 1])

        correctTheta = self.heading % 360
        theta = (correctTheta * 2 * math.pi) / 360

        self.location[0] = self.location[0] + (frameTime * self.speed * self.size) * math.cos(theta)
        self.location[1] = self.location[1] - (frameTime * self.speed * self.size) * math.sin(theta)


    # [1,−1]−2×(−1)×[0,1]=[1,−1]+2×[0,1]=[1,−1]+[0,2]
    def vector_reflect(self, normal):
        def mult(vectorA, vectorB):
            #return [(x, y) for x in vectorA for y in vectorB]
            return

        dir = self.heading
        rhs = 2 * (mult(mult(dir, normal), normal))
        return [dir[0] - rhs[0], dir[1] - rhs[1]]

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
                        self.size += int(math.sqrt((4/3)*math.pi*(individual.size)))
                        self.foodAmount += individual.foodAmount
                    elif(self.size < individual.size):
                        self.alive = False # being ate by target
                        individual.size += int(((4/3)*math.pi*(self.size))**(1./3.))
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
                self.size += int((4/3)*math.pi*(food.size)**(1./3.))

        self.speed = 100 / self.size

