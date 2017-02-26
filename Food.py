from random import randint

class FoodLst:

    def __init__(self,world_space, strength, num_foods, *args,**kwargs):
        self.worldSpace = world_space
        self.foodStrength = strength
        self.numFoods = num_foods

        self.foodsList = []
        self.create_food_list()

    def create_new_food(self,name,location):
        return Food(self.foodStrength,name,location)

    def remove(self, food):
        self.foodsList.remove(food)
        food = self.randLocation(food)
        food.alive = True
        self.foodsList.append(food)

    def add(self, food):
        self.foodsList.append(food)

    def randLocation(self, food):
        location = [randint(self.worldSpace[0], self.worldSpace[2]), randint(self.worldSpace[1], self.worldSpace[3])]
        food.location = location
        food.target = location
        return food

    def create_food_list(self):
        # numFood = int(WORLD_Y_SIZE * WORLD_X_SIZE * FOOD_DENSITY)

        for i in range(0, self.numFoods):
            x = randint(self.worldSpace[0], self.worldSpace[2])
            y = randint(self.worldSpace[1], self.worldSpace[3])
            newFood = self.create_new_food( i, [x, y])
            self.add(newFood)
            # foods.append(newFood)



class Food:

    def __init__(self,strength,name,location,*args,**kwargs):
        self.foodAmount = strength
        self.name = name
        self.location = location
        self.size = self.foodAmount/50
        self.alive = True
        self.color = '#9A7A00'
        self.typeName = -1


        self.target = location  #ignore DEBUG only
        self.heading = 0        #ignore DEBUG only
        self.nearest = []       #ignore DEBUG only
        self.needsText = False
        self.drawNearestLines = False

    def consume(self):
        self.alive = False
        return self.foodAmount
