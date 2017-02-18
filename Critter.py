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
