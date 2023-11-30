import numpy as np 
from matplotlib import pyplot as plt 

# generate terrain arrays, height 0 to 5
def terrain_generation(x,y):
    my_array = np.zeros([x, y]) 
    kx = float(x/1000)
    ky = float(y/1000)
    #border 
    my_array[int(1*ky):int(20*ky),:]= 5
    my_array[:,int(1*kx):int(20*kx)]=5
    my_array[int(979*ky):int(999*ky),:]=5
    my_array[:,int(979*kx):int(999*kx)]=5
    
    my_array[int(71*ky):int(104*ky),int(57*kx):int(160*kx)] = 2 
    my_array[int(189*ky):int(774*ky),int(127*kx):int(275*kx)] = 3 
    my_array[int(496*ky):int(574*ky),int(427*kx):int(875*kx)] = 1 
    my_array[int(597*ky):int(674*ky),int(527*kx):int(575*kx)] = 3 
    my_array[int(787*ky):int(894*ky), int(674*kx):int(943*kx)] = 4 

    return my_array
