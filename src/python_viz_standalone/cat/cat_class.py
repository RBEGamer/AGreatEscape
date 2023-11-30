import random
from random import choice
import numpy as np

# Moore neighborhood, for it contrains the center, so that count is at least 1
def count_neighbours(grid, row, col):
    count = 0
    for x, y in (
            (row - 1, col), (row + 1, col), (row, col),(row, col - 1),
            (row, col + 1), (row - 1, col - 1), (row - 1, col + 1),
            (row + 1, col - 1), (row + 1, col + 1)):
        if not (0 <= x < len(grid) and 0 <= y < len(grid[x])):
            # out of bounds
            continue
        if grid[x][y] == 1:
            count += 1
    return count

# if terrian height is over a threshold for the cat to jump over
def check_terrian(terrian, x, y, th, terrian_on):
    if terrian_on:
        if not (0 <= x < len(terrian) and 0 <= y < len(terrian[x])):
            return True
        else:
            if terrian[y][x] > th:
                return True
            else:
                return False
    else:
        return False

# if the presonality of current cat is happy with the scout of previous one
def check_personality_match(pre_grid_personality, self, interaction_on):
    if interaction_on:
        # timid cat will react slow
        if self.personality == "timid" and pre_grid_personality[self.pos[0]][self.pos[1]] != "void":
            speedup = 0.5
        # agreessive cat will always react heavily via speeding up
        elif self.personality == "agressive" and pre_grid_personality[self.pos[0]][self.pos[1]] != "void":
            speedup = 2
        elif self.personality == "social" and pre_grid_personality[self.pos[0]][self.pos[1]] == "agreesive":
            speedup = 1
        elif self.personality == "social" and pre_grid_personality[self.pos[0]][self.pos[1]] == "social":
            speedup = 1
        elif self.personality == "social" and pre_grid_personality[self.pos[0]][self.pos[1]] == "timid":
            speedup = 1
        else:
            speedup = 1
    else:
        speedup = 1
    return speedup

class Cat():
    # two attributes: personality and stages

    personality = ["timid","sociable","agressive"]
    stages = ["Kitten","Junior","Prime","Mature","Senior","Geriatric"]
    
    def __init__(self, pos):
        # random initialization
        self.pos = pos
        n = random.randint(0,2)
        self.personality = self.personality[n]
        n = random.randint(0,5)
        self.stages = self.stages[n]
    
    def stepChange(self, grid, daynight, terrian, pre_grid_personality, food, terrian_on, interaction_on, food_on):
        # direction to food
        direction0 = (food[0]-self.pos[0]) / np.sqrt(np.sum(np.square(food-self.pos)))
        direction1 = (food[1]-self.pos[1]) / np.sqrt(np.sum(np.square(food-self.pos)))
        if np.isnan(direction0):
            direction0 = 0
        if np.isnan(direction1):
            direction1 = 0
        # previous position backup
        tmp0 = self.pos[0]
        tmp1 = self.pos[1]
        # interaction calculation
        speedup = check_personality_match(pre_grid_personality, self, interaction_on)
        if self.stages == "Kitten":
            idx = 0
            while (self.pos[0] >= len(grid)) or (self.pos[0] < 0) or (self.pos[1] >= len(grid)) or (self.pos[1] < 0)  or (count_neighbours(grid, self.pos[0], self.pos[1])>=1) or check_terrian(terrian, self.pos[0], self.pos[1], 1, terrian_on):
                idx=idx + 1
                if food_on == False:
                    # Kitten move speed sets 15 with varies controling
                    self.pos[0] -= choice((-1, 1)) * random.randint(0,int(15*daynight*speedup + 3))
                    self.pos[1] -= choice((-1, 1)) * random.randint(0,int(15*daynight*speedup + 3))
                else:
                    self.pos[0] = int(direction0*15*daynight*speedup) +  self.pos[0]
                    self.pos[1] = int(direction1*15*daynight*speedup) +  self.pos[1]
                if idx == 4:
                    self.pos[0]=tmp0
                    self.pos[1]=tmp1
                    break;
            grid[self.pos[0]][self.pos[1]] = 1
            pre_grid_personality[self.pos[0]][self.pos[1]] = self.personality
        elif self.stages == "Junior":
            idx = 0
            while  (self.pos[0] >= len(grid)) or (self.pos[0] < 0) or (self.pos[1] >= len(grid)) or (self.pos[1] < 0)  or (count_neighbours(grid, self.pos[0], self.pos[1])>=1) or check_terrian(terrian, self.pos[0], self.pos[1], 2, terrian_on):
                idx=idx + 1
                if food_on == False:
                    # Junior move speed sets 25 with varies controling
                    self.pos[0] -= choice((-1, 1)) * random.randint(0,int(25*daynight*speedup + 3))
                    self.pos[1] -= choice((-1, 1)) * random.randint(0,int(25*daynight*speedup + 3))
                else:
                    self.pos[0] = int(direction0*25*daynight*speedup) +  self.pos[0]
                    self.pos[1] = int(direction1*25*daynight*speedup) +  self.pos[1]
                if idx == 4:
                    self.pos[0]=tmp0
                    self.pos[1]=tmp1
                    break;
            grid[self.pos[0]][self.pos[1]] = 1
            pre_grid_personality[self.pos[0]][self.pos[1]] = self.personality
        elif self.stages == "Prime":
            idx = 0
            while  (self.pos[0] >= len(grid)) or (self.pos[0] < 0) or (self.pos[1] >= len(grid)) or (self.pos[1] < 0)  or (count_neighbours(grid, self.pos[0], self.pos[1])>=1) or check_terrian(terrian, self.pos[0], self.pos[1], 3, terrian_on):
                idx=idx + 1
                if food_on == False:
                    # Prime move speed sets 45 with varies controling
                    self.pos[0] -= choice((-1, 1)) * random.randint(0,int(45*daynight*speedup + 3))
                    self.pos[1] -= choice((-1, 1)) * random.randint(0,int(45*daynight*speedup + 3))
                else:
                    self.pos[0] = int(direction0*45*daynight*speedup) +  self.pos[0]
                    self.pos[1] = int(direction1*45*daynight*speedup) +  self.pos[1]
                if idx == 4:
                    self.pos[0]=tmp0
                    self.pos[1]=tmp1
                    break;
            grid[self.pos[0]][self.pos[1]] = 1
            pre_grid_personality[self.pos[0]][self.pos[1]] = self.personality
        elif self.stages == "Mature":
            idx = 0
            while  (self.pos[0] >= len(grid)) or (self.pos[0] < 0) or (self.pos[1] >= len(grid)) or (self.pos[1] < 0)  or (count_neighbours(grid, self.pos[0], self.pos[1])>=1) or check_terrian(terrian, self.pos[0], self.pos[1], 4, terrian_on):
                idx=idx + 1
                if food_on == False:
                     # Mature move speed sets 45 with varies controling
                    self.pos[0] -= choice((-1, 1)) * random.randint(0,int(45*daynight*speedup + 3))
                    self.pos[1] -= choice((-1, 1)) * random.randint(0,int(45*daynight*speedup + 3))
                else:
                    self.pos[0] = int(direction0*45*daynight*speedup) +  self.pos[0]
                    self.pos[1] = int(direction1*45*daynight*speedup) +  self.pos[1]
                if idx == 4:
                    self.pos[0]=tmp0
                    self.pos[1]=tmp1
                    break;
            grid[self.pos[0]][self.pos[1]] = 1
            pre_grid_personality[self.pos[0]][self.pos[1]] = self.personality
        elif self.stages == "Senior":
            idx = 0
            while  (self.pos[0] >= len(grid)) or (self.pos[0] < 0) or (self.pos[1] >= len(grid)) or (self.pos[1] < 0)  or (count_neighbours(grid, self.pos[0], self.pos[1])>=1) or check_terrian(terrian, self.pos[0], self.pos[1], 3, terrian_on):
                idx=idx + 1     
                if food_on == False:
                    # Senior move speed sets 25 with varies controling
                    self.pos[0] -= choice((-1, 1)) * random.randint(0,int(25*daynight*speedup + 3))
                    self.pos[1] -= choice((-1, 1)) * random.randint(0,int(25*daynight*speedup + 3))
                else:
                    self.pos[0] = int(direction0*25*daynight*speedup) +  self.pos[0]
                    self.pos[1] = int(direction1*25*daynight*speedup) +  self.pos[1]
                if idx == 4:
                    self.pos[0]=tmp0
                    self.pos[1]=tmp1
                    break;
            grid[self.pos[0]][self.pos[1]] = 1
            pre_grid_personality[self.pos[0]][self.pos[1]] = self.personality
        else:
            idx = 0
            while  (self.pos[0] >= len(grid)) or (self.pos[0] < 0) or (self.pos[1] >= len(grid)) or (self.pos[1] < 0) or (count_neighbours(grid, self.pos[0], self.pos[1])>=1) or check_terrian(terrian, self.pos[0], self.pos[1], 2, terrian_on):
                idx=idx + 1       
                if food_on == False:
                    # Geriatric move speed sets 15 with varies controling
                    self.pos[0] -= choice((-1, 1)) * random.randint(0,int(15*daynight*speedup + 3))
                    self.pos[1] -= choice((-1, 1)) * random.randint(0,int(15*daynight*speedup + 3))
                else:
                    self.pos[0] = int(direction0*15*daynight*speedup) +  self.pos[0]
                    self.pos[1] = int(direction1*15*daynight*speedup) +  self.pos[1]
                if idx == 4:
                    self.pos[0]=tmp0
                    self.pos[1]=tmp1
                    break;
            grid[self.pos[0]][self.pos[1]] = 1
            pre_grid_personality[self.pos[0]][self.pos[1]] = self.personality
        return grid, pre_grid_personality

    # color indicates personality
    def getColor(c):
        if c.personality == "timid":
            color = 'limegreen'
        elif c.personality == "sociable":
            color = 'royalblue'
        else:
            color = 'orangered'
        return color

    # size indicates stages(ages)             
    def getSize(c):
        if c.stages == "Kitten":
            size = 10
        elif c.stages == "Junior":
            size = 20
        elif c.stages == "Prime":
            size = 30
        elif c.stages == "Mature":
            size = 40
        elif c.stages == "Senior":
            size = 50
        else:
            size = 60
        return size