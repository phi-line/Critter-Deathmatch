from random import randint

class Food:

    def __init__(self,strength,name,location,*args,**kwargs):
        self.foodAmount = strength
        self.name = name
        self.location = location
        self.size = self.foodAmount/100
        self.alive = True
        self.color = '#9A7A00'
        self.typeName = -1

    def consume(self):
        #print('CONSUMED: ',self.name)
        #self.alive = False
        self.location[0] = randint(50, 1150)
        self.location[1] = randint(50, 550)
        self.foodAmount += (randint(0,100)-50)
        if randint(0,100) < 20:
            self.alive = False
        #print(self.location[0],'\t',self.location[1])
        return self.foodAmount