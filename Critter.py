import math

class Critter:
    def __init__(self, *args,**kwargs):
        self.foodAmount
        self.foodDecayRate
        self.size
        self.divideSize
        self.turnSpeedVector
        self.detectDistance
        self.heading = 0
        self.location = [0,0]
        self.color
        self.name
        self.speed = 1
        self.alive = True
        self.typeName
        self.touching = False
        self.needs_update = False
        self.whoTouching
        self.gen = 0

    def move(self, frameTime):
        theta = (self.heading * 2 * math.pi) / 360
        self.location[0] = (self.speed*frameTime)*math.cos(theta) + self.location[0]
        self.location[1] = (self.speed*frameTime)*math.sin(theta) + self.location[1]
