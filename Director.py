import math
import time
import tkinter as tk
from random import randint, seed

import AI
from GUI import GUI
from Specie import Specie
from Critter import Critter
from Food import Food
from Food import FoodLst
from Squad import Squad

NUM_SPECIES = 10
STARTING_POPULATION = 1

#FOOD_DENSITY = 0.000075
FOOD_DENSITY = 75
FOOD_STRENGTH = 200

FRAME_TIME = 0.02

WINDOW_X_SIZE = 1200
WINDOW_Y_SIZE = 600

WORLD_X_MIN = 0
WORLD_Y_MIN = 0
WORLD_X_MAX = 1200 #canvas_x
WORLD_Y_MAX = 600  #canvas_y

display_x_min = WORLD_X_MIN
display_y_min = WORLD_Y_MIN
display_x_max = WORLD_X_MAX
display_y_max = WORLD_Y_MAX

def main():
    seed()

    world_space = [WORLD_X_MIN,WORLD_Y_MIN,WORLD_X_MAX,WORLD_Y_MAX]
    screen_location = [display_x_min,display_y_min,display_x_max,display_y_max]

    gui = GUI(tk.Tk(),WINDOW_X_SIZE,WINDOW_Y_SIZE)
    gui.place_window(screen_location[0],screen_location[1],screen_location[2],screen_location[3])

    foods = FoodLst(world_space,FOOD_STRENGTH,FOOD_DENSITY)

    species = []
    #foods = foodListHolder.foodsList
    print(foods)

    for i in range(0,NUM_SPECIES):
        #newSpecie = Specie(startingPopulation=STARTING_POPULATION,typeName="species" + str(i))
        newSpecie = Specie(startingPopulation=STARTING_POPULATION, typeName=i, frama_time=FRAME_TIME, world_space=world_space)
        species.append(newSpecie)

    main_loop(world_space,screen_location,gui,species,foods)



def main_loop(world_space,screen_location, gui,species,foods):
    x = 0
    while x == 0:
        logic(species,foods)
        draw(world_space,screen_location,gui,species,foods)
        time.sleep(FRAME_TIME)

def logic(species, foods):

    #individualsToUpdate = []
    for specie in species:
        specie.determine_birth()
        for individual in specie.individuals:
            if individual.alive:
                AI.decide_action(individual,species,foods)
                individual.move()
                individual.check_state(species,foods)
                Squad.join(individual)
            else:
                specie.individuals.remove(individual)

    for specie in species:
        for individual in specie.individuals:
            if individual.alive:
                individual.update(speciesLst=species, foodLst=foods)

    for squad in Squad.squadLst:
        squad.update()

def draw(world_space, screen_location, gui, species, foods):
    gui.clear()
    gui.place_window(screen_location[0], screen_location[1], screen_location[2], screen_location[3])
    gui.draw_world_borders(world_space)

    for food in foods.foodsList:
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
        obj.needsText = False
        obj.drawNearestLines = False
        for m in squad.members:
            obj.target = m.location
            gui.debug_overlay(obj)
        gui.add_object_to_draw(squad)

    gui.draw()

main()