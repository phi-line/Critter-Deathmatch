class Food:

    def __init__(self,name,location,*args,**kwargs):
        self.foodAmount = 100
        self.name = name
        self.location = location
        self.size = self.foodAmount/10
        self.alive = True
        color = '#9A7A00'

