import csv
import cv2
import numpy as np
from numpy import genfromtxt

my_data = genfromtxt('floorplan.csv', delimiter=',')
height = my_data.shape[0]
width = my_data.shape[1]

my_index = np.zeros(my_data.shape)
index = -1
for x in range(0,height):
    for y in range(0,width):        
        if my_data[x,y] == 2 or my_data[x,y] == 3:
            if x == 0 and y== 0:
                continue
            if x == 0 and y!= 0:
                if my_data[x,y]!= my_data[x,y-1]:
                    index = index+1
                    my_index[x,y] = index
            if y == 0 and x!= 0:
                if my_data[x,y]!= my_data[x-1,y]:
                    index = index+1
                    my_index[x,y] = index
            else:
                if my_data[x,y]!= my_data[x,y-1] and my_data[x,y]!= my_data[x-1,y]:
                    index = index+1
                    my_index[x,y] = index#

unique, counts = np.unique(my_index, return_counts=True)

for i in unique:
    if i > 0:
        for x in range(0,height):
            for y in range(0,width):   
                if my_data[x,y] == my_data[x,y-1] and (my_data[x,y] == 2 or my_data[x,y]==3):
                    my_index[x,y] = my_index[x,y-1]
                if my_data[x,y] == my_data[x-1,y] and (my_data[x,y] == 2 or my_data[x,y]==3):
                    my_index[x,y] = my_index[x-1,y]

unique, counts = np.unique(my_index, return_counts=True)
print(np.asarray((unique, counts)).T)
print(len(unique))

result = []
for i in unique:
    if i > 0:
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
                    if my_data[x,y] == 2:
                        is_special=True
                    else:
                        is_special=False
        result.append({"x":int(x_sum/n),"y":int(y_sum/n),"special":is_special})
        

print(result)    

