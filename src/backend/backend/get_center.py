import csv
import cv2
import numpy as np
from numpy import genfromtxt

def get_center(_map):

    height = _map.shape[0]
    width = _map.shape[1]

    my_index = np.zeros(_map.shape)
    index = -1
    for x in range(0,height):
        for y in range(0,width):
            if _map[x,y] == 2 or _map[x,y]==3:
                if _map[x,y]!= _map[x,y-1] and _map[x,y]!= _map[x-1,y]:
                    index = index+1
                my_index[x,y] = index
            

    for x in range(0,height):
        for y in range(0,width):   
            if _map[x,y] == _map[x,y-1] and (_map[x,y] == 2 or _map[x,y]==3):
                my_index[x,y] = my_index[x,y-1]
        if _map[x,y] == _map[x-1,y] and (_map[x,y] == 2 or _map[x,y]==3):
            my_index[x,y] = my_index[x-1,y]

    unique, counts = np.unique(my_index, return_counts=True)
    #print(np.asarray((unique, counts)).T)
    #print(len(unique))

    result = []
    for i in unique:
        is_special = False
        x_sum = 0
        y_sum = 0
        n = 0
        for x in range(0, height):
            for y in range(0, width):
                if my_index[x,y] == i:
                    x_sum = x+x_sum
                    y_sum = y+y_sum
                    n = n+1
                    if _map[x,y] == 3:
                        is_special=True
                    else:
                        is_special=False
        result.append({"x": int(x_sum/n),"y": int(y_sum/n), "special": is_special})
    return result 


#get_center("../map/floorplan.csv")