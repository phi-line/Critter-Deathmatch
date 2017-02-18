import math
import time
import tkinter as tk

from GUI import GUI
from Specie import Specie
from Critter import Critter
from Food import Food

NUM_SPECIES = 2
STARTING_POPULATION = 100
FRAME_TIME = 0.05
WORLD_X_SIZE = 600
WORLD_Y_SIZE = 600


def main():
    gui = GUI(tk.Tk(),WORLD_X_SIZE,WORLD_Y_SIZE)
    species = []

    for newSpecie in (0,NUM_SPECIES):
        newSpecie = Specie(STARTING_POPULATION)
        species.append(newSpecie)

    main_loop(gui,species)

def main_loop(gui,species):
    while True:
        logic(species)
        draw(gui,species)
        time.sleep(FRAME_TIME)

def logic(species):
    individualsToUpdate = []

    for specie in species:
        for individual in specie.individuals:
            if individual.alive:
                individual.decide_action(species)
                individual.move(FRAME_TIME)
                individual.check_state()
                if individual.needs_update:
                    individualsToUpdate.append(individual)

    for individual in individualsToUpdate:
        if individual.alive:
            individual.update()

def draw(gui, species):
    for specie in species:
        for individual in specie:
            gui.add_object_to_draw(individual)
    gui.draw()

main()