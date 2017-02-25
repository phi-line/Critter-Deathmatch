import math
import time
import tkinter as tk
from random import randint, seed

from GUI import GUI
from Specie import Specie
from Critter import Critter
from Food import Food

NUM_SPECIES = 5
STARTING_POPULATION = 1
FRAME_TIME = 0.02
WORLD_X_SIZE = 1200 #canvas_x
WORLD_Y_SIZE = 600  #canvas_y
CANVAS_X = 1200
CANVAS_Y = 600
#FOOD_DENSITY = 0.000075
FOOD_DENSITY = 75
FOOD_STRENGTH = 400

def main():
    seed()

    gui = GUI(tk.Tk(),WORLD_X_SIZE,WORLD_Y_SIZE)
    species = []
    foods = create_foods()

    for i in range(0,NUM_SPECIES):
        #newSpecie = Specie(startingPopulation=STARTING_POPULATION,typeName="species" + str(i))
        newSpecie = Specie(startingPopulation=STARTING_POPULATION, typeName=i)
        species.append(newSpecie)

    main_loop(gui,species,foods)

def create_foods():
    #numFood = int(WORLD_Y_SIZE * WORLD_X_SIZE * FOOD_DENSITY)
    numFood = FOOD_DENSITY
    foods = []
    for i in range(0,numFood):
        x = randint(50,WORLD_X_SIZE-50)
        y = randint(50,WORLD_Y_SIZE-50)
        newFood = Food(FOOD_STRENGTH,i,[x,y])
        foods.append(newFood)
    return foods

def main_loop(gui,species,foods):
    while True:
        logic(species,foods)
        draw(gui,species,foods)
        time.sleep(FRAME_TIME)

def logic(species, foods):

    #individualsToUpdate = []
    for specie in species:
        specie.determine_birth()
        for individual in specie.individuals:
            if individual.alive:
                individual.decide_action(species,foods)
                individual.move(FRAME_TIME)
                individual.check_state(species,foods)
                #if individual.needs_update:
                #   individualsToUpdate.append(individual)

    for specie in species:
        for individual in specie.individuals:
            if individual.alive:
                individual.update(frameTime=FRAME_TIME,speciesLst=species, foodLst=foods)

def draw(gui, species, foods):
    gui.clear()

    for food in foods:
        if(food.alive):
            gui.add_object_to_draw(food)

    for specie in species:
        for individual in specie.individuals:
            if(individual.alive):
                gui.add_object_to_draw(individual)

    gui.draw()

main()