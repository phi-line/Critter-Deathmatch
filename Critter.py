class Critter:
    def __init__(self, location, *args,**kwargs):
        self.size = 1
        self.foodAmount
        self.foodDecayRate = .01
        self.divideSize = 1.5 * self.size # 1.5 * start size
        self.turnSpeedVector = 45  # deg / sec (45 / sec)
        self.detectDistance = self.size + (2 * self.size)
        self.directionVector = [0, 0]
        self.location = location
        self.color = self.color = "#00FF00"
        self.name = "default_name"
        self.speed = 1
        self.alive = True
        self.typeName = "critter"
        self.touching = False
        self.needs_update = False
        self.whoTouching = []
        self.gen = 0

    def move(self, newLocation):
        '''
        replace current location with new one
        :param newLocation: list of x,y
        :return: none
        '''
        self.location[0] = newLocation[0]
        self.location[1] = newLocation[1]

    def decide_action(self, speciesLst, foodLst):
        '''
        decide action based on knowledge of species and food
        :param speciesLst: list of species
        :param foodLst: list of food
        :return: none
        '''
        self.directionVector = 180 # to the left for demo
        pass

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

    def check_state(self):
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

