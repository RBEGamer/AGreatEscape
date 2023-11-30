import csv
import cv2
import numpy as np
from numpy import genfromtxt

my_data = genfromtxt('floorplan.csv', delimiter=',')
my_data_2 = my_data.copy()

height = my_data.shape[0]
width = my_data.shape[1]

my_index = np.zeros(my_data.shape)
index = -1
for x in range(0,height):
    for y in range(0,width):
        if my_data[x,y] == 2 or my_data[x,y]==3:
            if my_data[x,y]!= my_data[x,y-1] and my_data[x,y]!= my_data[x-1,y]:
                index = index+1
            my_index[x,y] = index
        

for x in range(0,height):
    for y in range(0,width):   
        if my_data[x,y] == my_data[x,y-1] and (my_data[x,y] == 2 or my_data[x,y]==3):
            my_index[x,y] = my_index[x,y-1]
    if my_data[x,y] == my_data[x-1,y] and (my_data[x,y] == 2 or my_data[x,y]==3):
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
                if my_data[x,y] == 3:
                    is_special=True
                else:
                    is_special=False
    result.append({"x":int(x_sum/n),"y":int(y_sum/n),"special":is_special})

#print(result)
#viz map

my_map = np.zeros((height,width,3), np.uint8)
for x in range(0,height):
    for y in range(0,width):
        if my_data_2[x,y] == 2:
            my_map[x,y] = (0,255,0)
        if my_data_2[x,y] == 3:
            my_map[x,y] = (255,0,0)
        if my_data_2[x,y] == 0:
            my_map[x,y] = (100,100,100)
        if my_data_2[x,y] == -1:
            my_map[x,y] = (150,150,150)
        if my_data_2[x,y] == 1:
            my_map[x,y] = (255,255,255)
#gray = cv2.cvtColor(my_map, cv2.COLOR_BGR2GRAY)

cv2.imshow("my_map",my_map)
cv2.waitKey()