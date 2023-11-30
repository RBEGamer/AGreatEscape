import random
import numpy as np

# generate random food location
def food_generate(XMAX, YMAX):
    randX = random.randint(0,XMAX)
    randY = random.randint(0,YMAX)
    food_spot = np.array([randX, randY])
    return food_spot
