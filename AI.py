import math
from random import randint

def decide_action(individual, species, foods):
    update_nearest(individual, species, foods)
    update_imperative(individual)
    point_heading(individual)

def update_nearest(individual, species, foods):
    if individual.nearest_empty:
        individual.init_nearest(species, foods)

    for food in foods.foodsList:
        individual.compare_near_food(food)

    for specie in species:
        for individual in specie.individuals:
            if individual.alive:
                if (individual.typeName == individual.typeName and individual.name != individual.name):
                    individual.compare_near_friend(individual)
                else:
                    if individual.size > individual.size:
                        individual.compare_near_large(individual)
                    elif individual.size < individual.size:
                        individual.compare_near_small(individual)

def update_imperative(individual):
    if individual.size <= 0:
        return

    large = -1
    food = -1
    small = -1
    friend = -1

    largeMod = individual.flee_scalar  # flee
    foodMod = individual.food_scalar  # food
    smallMod = individual.hunt_scalar  # hunt
    friendMod = individual.flock_scalar  # flock

    largeSeparation = (individual.distance(individual.nearest[0]) / (individual.detectDistance * individual.size))
    foodSeparation = (individual.distance(individual.nearest[1]) / (individual.detectDistance * individual.size))
    smallSeparation = (individual.distance(individual.nearest[2]) / (individual.detectDistance * individual.size))
    friendSeparation = (individual.distance(individual.nearest[3]) / (individual.detectDistance * individual.size))

    individual.mostImperativeIndex = -1

    if individual.nearest[0].alive and largeSeparation <= 1 and largeSeparation > 0:
        large = 1.0 - (individual.distance(individual.nearest[0]) / (individual.detectDistance * individual.size))
        large *= largeMod

    if individual.nearest[1].alive and foodSeparation <= 1 and foodSeparation > 0:
        # print(individual.distance(individual.nearest[1]))
        food = 1.0 - (individual.distance(individual.nearest[1]) / (individual.detectDistance * individual.size))
        food *= abs(1.0 - (individual.foodAmount / (individual.birthFoodAmount * individual.divideSize)))
        food *= foodMod

    if individual.nearest[2].alive and smallSeparation <= 1 and smallSeparation > 0:
        small = 1.0 - (individual.distance(individual.nearest[2]) / (individual.detectDistance * individual.size))
        small *= smallMod

    if individual.nearest[3].alive and friendSeparation <= 1 and friendSeparation > 0:
        friend = 1.0 - (individual.distance(individual.nearest[3]) / (individual.detectDistance * individual.size))
        friend *= friendMod

    #print('name: ',individual.typeName,',',individual.name,'\t',large,'\t',food,'\t',small,'\t',friend)

    # find the largest value from above
    if (large > 0 and large > food and large > small and large > friend):
        individual.mostImperativeIndex = 0
    elif (food > 0 and food > large and food > small and food > friend):
        individual.mostImperativeIndex = 1
    elif (small > 0 and small > large and small > food and small > friend):
        individual.mostImperativeIndex = 2
    elif (friend > 0 and friend > large and friend > food and friend > small):
        individual.mostImperativeIndex = 3
    else:
        individual.mostImperativeIndex = individual.mostImperativeIndex

    if (individual.mostImperativeIndex >= 0):
        if individual.nearest[individual.mostImperativeIndex].size == individual.size:
            individual.mostImperativeIndex = 1

        if individual.nearest[individual.mostImperativeIndex].typeName == individual.typeName:
            if individual.nearest[individual.mostImperativeIndex].name != individual.name:
                individual.mostImperativeIndex = 3

        if not individual.nearest[individual.mostImperativeIndex].alive:
            individual.mostImperativeIndex = 1

        #individual.mostImperativeIndex = 0
        #if(individual.mostImperativeIndex == 0):
            #print('name: ', individual.typeName, ',', individual.name, '\t', large, '\t', food, '\t', small, '\t', friend)

        individual.target = individual.nearest[individual.mostImperativeIndex].location
    else:
        individual.mostImperativeIndex = -1

        # print(individual.mostImperativeIndex)

def point_away_from_large(individual):
    # print('point_away_from_large')
    x = -1 * int(individual.nearest[0].location[0] - individual.location[0])
    y = int(individual.nearest[0].location[1] - individual.location[1])

    if (x == 0):
        if (y < 0):
            # print("y<0")
            targetTheta = 270
        else:
            # print("y>0")
            targetTheta = 90
    else:
        ratio = y / x
        targetTheta = math.atan(ratio)
        targetTheta = int((targetTheta * 180) / math.pi)

    # print(x,'\t',y)
    # print(targetTheta)
    if (x < 0):
        targetTheta = targetTheta + 180

    if (targetTheta < 0):
        targetTheta = targetTheta + 360
    # print(targetTheta)
    # print('frame end\n')
    # individual.speed +=0.1
    if individual.speed > 12:
        individual.speed = 12
    individual.heading = targetTheta - individual.heading / randint(180, 360)


def point_at_food(individual):
    # print('name: ',individual.nearest[1].name)
    x = int(individual.nearest[1].location[0] - individual.location[0])
    y = -1 * int(individual.nearest[1].location[1] - individual.location[1])

    if (x == 0):
        if (y < 0):
            # print("y<0")
            targetTheta = 270
        else:
            # print("y>0")
            targetTheta = 90
        return
    else:
        ratio = y / x
        targetTheta = math.atan(ratio)
        targetTheta = int((targetTheta * 180) / math.pi)

    # print(individual.heading,'\t',x,'\t',y)
    # print(targetTheta)
    if (x < 0):
        targetTheta = targetTheta + 180

    if (targetTheta < 0):
        targetTheta = targetTheta + 360
    # print(targetTheta)
    # print('frame end\n')

    individual.heading = targetTheta
    # print(individual.name,'\t',x, ' \t', y,'\t',individual.heading)


def point_at_small(individual):
    # print('point_at_small')
    if individual.size > individual.nearest[2].size:
        point_at_food(individual)
        return
    x = int(individual.nearest[2].location[0] - individual.location[0])
    y = -1 * int(individual.nearest[2].location[1] - individual.location[1])

    if (x == 0):
        if (y < 0):
            # print("y<0")
            targetTheta = 270
        else:
            # print("y>0")
            targetTheta = 90
    else:
        ratio = y / x
        targetTheta = math.atan(ratio)
        targetTheta = int((targetTheta * 180) / math.pi)

    # print(x,'\t',y)
    # print(targetTheta)
    if (x < 0):
        targetTheta = targetTheta + 180

    if (targetTheta < 0):
        targetTheta = targetTheta + 360
    # print(targetTheta)
    # print('frame end\n')

    individual.heading = targetTheta


def point_with_friend(individual):
    #print('point_with_friend')
    x = int(individual.nearest[3].location[0] - individual.location[0])
    y = -1 * int(individual.nearest[3].location[1] - individual.location[1])

    if (x == 0):
        if (y < 0):
            # print("y<0")
            targetTheta = 270
        else:
            # print("y>0")
            targetTheta = 90
    else:
        ratio = y / x
        targetTheta = math.atan(ratio)
        targetTheta = int((targetTheta * 180) / math.pi)

    # print(x,'\t',y)
    # print(targetTheta)
    if (x < 0):
        targetTheta = targetTheta + 180

    if (targetTheta < 0):
        targetTheta = targetTheta + 360
    # print(targetTheta)
    # print('frame end\n')

    individual.heading = individual.heading - targetTheta/randint(36,72)


def point_heading(individual):
    if individual.mostImperativeIndex == 0:
        point_away_from_large(individual)
    elif individual.mostImperativeIndex == 1:
        point_at_food(individual)
    elif individual.mostImperativeIndex == 2:
        point_at_small(individual)
    elif individual.mostImperativeIndex == 3:
        point_with_friend(individual)
    else:
        # print('critter[',individual.name,'] has no target')
        individual.target = individual.location
        individual.heading += (randint(0, 10) - 5)