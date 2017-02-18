class Food:

    def __init__(self,strength,name,location,*args,**kwargs):
        self.foodAmount = strength
        self.name = name
        self.location = location
        self.size = self.foodAmount/20
        self.alive = True
        self.color = '#9A7A00'

    def consume(self):
        self.alive = False
        return self.foodAmount