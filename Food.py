from random import randint

class FoodLst:

    def __init__(self, strength, *args,**kwargs):

        self.foodLst = []

    def remove(self, food):
        self.foodLst.remove(food)
        food = self.randLocation(food)
        self.foodLst.append(food)

    def add(self, food):
        self.foodLst.append(food)

    def randLocation(self, food):
        location = [randint(50, 1150), randint(50, 550)]
        food.location = location
        return food


class Food:

    def __init__(self,strength,name,location,*args,**kwargs):
        self.foodAmount = strength
        self.name = name
        self.location = location
        self.target = location  #ignore DEBUG only
        self.heading = 0        #ignore DEBUG only
        self.size = self.foodAmount/50
        self.alive = True
        self.color = '#9A7A00'
        self.typeName = -1

    def consume(self):
        self.alive = False
        return self.foodAmount
