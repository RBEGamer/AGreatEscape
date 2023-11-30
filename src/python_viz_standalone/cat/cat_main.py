import random
import matplotlib.pyplot as plt
import numpy as np
import time
from cat_class import Cat
from matplotlib.widgets import Slider, Button, RadioButtons
from terrain_generation import terrain_generation
import argparse
from food_generate import food_generate
from datetime import datetime

# sample run0: "python3 cat_main.py "
# sample run1: "python3 cat_main.py -dim 2000 -num 30"
# sample run2: "python3 cat_main.py -terrain_on True"
# sample run3: "python3 cat_main.py -h"

# parameters
parser = argparse.ArgumentParser(description='Cats Simulations')
parser.add_argument('--dim', type=int, default=1000, help='length in x and y asix')
parser.add_argument('--num', type=int, default=20, help='number of cats')
parser.add_argument('--terrain_on', type=bool, default=False, help='is terrain turned on')
parser.add_argument('--interaction_on', type=bool, default=False, help='is Interaction turned on')
parser.add_argument('--food_on', type=bool, default=False, help='is Food turned on')
args = parser.parse_args()

# grid size
XMAX = args.dim
YMAX = XMAX
# cats number
NUM = args.num

def main():

    #event_flag
    terrain_on = args.terrain_on
    interaction_on = args.interaction_on
    food_on = args.food_on
    save_on = False

    # get object instances in one list
    cats_list = []
    # grid to calculte neibourhoods
    grid = [[0 for x in range(YMAX+1)] for y in range(XMAX+1)]
    # grid save personality of cats
    pre_grid_personality = [["void" for x in range(YMAX+1)] for y in range(XMAX+1)]
    
    # cats initilization
    for i in range(NUM):
        randX = random.randint(0,XMAX)
        randY = random.randint(0,YMAX)
        cats_list.append(Cat([randX,randY]))
        grid[randX][randY] = 1
        pre_grid_personality[randX][randY] = Cat([randX,randY]).personality


    # load terrain
    terrain = terrain_generation(YMAX, XMAX)

    # load food
    food = food_generate(XMAX, YMAX)
    food_x = food[0]
    food_y = food[1]
    food_c = "orange"
    food_size = 200

    plt.ion()

    # loop over 600 frames, 0-200: move, 200-300: add terrain, 
    # 300-400: add interaction, 400-500 add food, 500-600 remove food
    for i in range(600):
        if i%100 == 1 or i%100 == 95:
            save_on = True
        else:
            save_on = False
        if i >= 200 and i <300:
            terrain_on = True
            interaction_on = False
            food_on = False
        elif i>300 and i<400:
            terrain_on = True
            interaction_on = True
            food_on = False
        elif i>=400 and i<500:
            terrain_on = True
            interaction_on = True
            food_on = True
        elif i>=500 and i<600:
            terrain_on = True
            interaction_on = True
            food_on = False


        print("\n ### TIMESTEP ",i, "###")
        # AM/PM active level smooth changing
        if i%100 > 50:
            daynight = 2-(i%50)*2/50 + 0.1
        else:
            daynight = (i%50)*2/50 + 0.1
        xvalues = []
        yvalues = []
        sizes = []
        sizes_unit = []
        colors = []
        for m in cats_list:
            # step Change controlled by flags
            grid, pre_grid_personality = m.stepChange( grid, daynight, terrain, pre_grid_personality, food, terrain_on, interaction_on, food_on)
            xvalues.append(m.pos[0])
            yvalues.append(m.pos[1])
            sizes.append(m.getSize())
            sizes_unit.append(1)
            colors.append(m.getColor())
        
        # plot cats and move event
        plt.scatter(xvalues, yvalues, s=sizes,c=colors,alpha=0.4)
        plt.scatter(xvalues, yvalues, s=sizes_unit,c=colors)
        plt.figtext(0.2, 0.02, "move AM/PM", ha="center", fontsize=8, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

        # plot interaction event
        if interaction_on:
            plt.figtext(0.42, 0.02, "interaction", ha="center", fontsize=8, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

        # plot food and food event
        if food_on:
            plt.scatter(food_x, food_y, s=food_size, c=food_c)
            plt.scatter(food_x, food_y, s=food_size*2, c="beige", alpha=0.4)
            plt.scatter(food_x, food_y, s=food_size*4, c="darkslategrey", alpha=0.2)
            plt.figtext(0.53, 0.02, "food", ha="center", fontsize=8, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

        # plot terrain and terrain event
        if terrain_on:
            plt.imshow(255-terrain*50, cmap='gray', vmin=0, vmax=255)
            plt.figtext(0.31, 0.02, "terrain", ha="center", fontsize=8, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

        plt.xlim(0,XMAX)
        plt.ylim(0,YMAX)
        plt.gca().set_aspect('equal', adjustable='box')

        # save definded frames
        if save_on:
            print('saving plot...')
            date = datetime. now(). strftime("%Y_%m_%d-%I:%M:%S_%p")
            plt.savefig(date+'.png')

        plt.draw()
        # for animation
        plt.pause(0.004)
        plt.clf()
    
if __name__ == "__main__":
    main()