import math
import time
import tkinter as tk
from random import randint, seed

from GUI import GUI
from Specie import Specie
from Critter import Critter
from Food import Food
from Food import FoodLst
from Squad import Squad

NUM_SPECIES = 2
STARTING_POPULATION = 1
FRAME_TIME = 0.02
WORLD_X_SIZE = 1200 #canvas_x
WORLD_Y_SIZE = 600  #canvas_y
WINDOW_X_SIZE = 1200
WINDOW_Y_SIZE = 600
#FOOD_DENSITY = 0.000075
FOOD_DENSITY = 20
FOOD_STRENGTH = 200

display_x_min = 0
display_y_min = 0
display_x_max = WORLD_X_SIZE
display_y_max = WORLD_Y_SIZE

def main():
    seed()

    screen_location = [display_x_min,display_y_min,display_x_max,display_y_max]

    gui = GUI(tk.Tk(),WINDOW_X_SIZE,WINDOW_Y_SIZE)
    gui.place_window(screen_location[0],screen_location[1],screen_location[2],screen_location[3])

    species = []
    foods = create_foods()
    print(foods)

    for i in range(0,NUM_SPECIES):
        #newSpecie = Specie(startingPopulation=STARTING_POPULATION,typeName="species" + str(i))
        newSpecie = Specie(startingPopulation=STARTING_POPULATION, typeName=i, frama_time=FRAME_TIME)
        species.append(newSpecie)

    main_loop(screen_location,gui,species,foods)

def create_foods():
    #numFood = int(WORLD_Y_SIZE * WORLD_X_SIZE * FOOD_DENSITY)
    numFood = FOOD_DENSITY
    foods = FoodLst(FOOD_STRENGTH)
    for i in range(0,numFood):
        x = randint(50,WORLD_X_SIZE-50)
        y = randint(50,WORLD_Y_SIZE-50)
        newFood = Food(FOOD_STRENGTH,i,[x,y])
        foods.add(newFood)
        #foods.append(newFood)
    return foods

def main_loop(screen_location, gui,species,foods):
    while True:
        logic(species,foods)
        draw(screen_location,gui,species,foods)
        time.sleep(FRAME_TIME)

def logic(species, foods):

    #individualsToUpdate = []
    for specie in species:
        specie.determine_birth()
        for individual in specie.individuals:
            if individual.alive:
                individual.decide_action(species,foods)
                individual.move()
                individual.check_state(species,foods)
                Squad.join(individual)
                #if individual.needs_update:
                #   individualsToUpdate.append(individual)

    for specie in species:
        for individual in specie.individuals:
            if individual.alive:
                individual.update(speciesLst=species, foodLst=foods)

    for squad in Squad.squadLst:
        squad.update()

def draw(screen_location, gui, species, foods):
    gui.clear()
    gui.place_window(screen_location[0], screen_location[1], screen_location[2], screen_location[3])

    for food in foods.foodLst:
        if(food.alive):
            gui.add_object_to_draw(food)
        else:
            foods.remove(food)

    for specie in species:
        for individual in specie.individuals:
            if(individual.alive):
                gui.add_object_to_draw(individual)

    for squad in Squad.squadLst:
        center = squad.center()
        class Obj:
            pass
        obj = Obj()
        obj.heading = 0
        obj.color = '#999999'
        obj.location = center
        obj.size = 5
        for m in squad.members:
            obj.target = m.location
            gui.debug_overlay(obj)
        gui.add_object_to_draw(squad)

    gui.draw()

main()