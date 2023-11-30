import csv
import cv2
import numpy as np
from numpy import genfromtxt
import numpy as np
from numpy import genfromtxt
import heapq


my_data = genfromtxt('floorplan.csv', delimiter=',')
my_data_2 = my_data.copy()
height = my_data.shape[0]
width = my_data.shape[1]

my_index = np.zeros(my_data.shape)
index = -1
old = -1
for x in range(0,height):
    for y in range(0,width):        
        if my_data[x,y] == 2 and (my_data[x,y] == old or head):
            if x == 0 and y== 0:
                continue
            if x == 0 and y!= 0:
                if my_data[x,y]!= my_data[x,y-1]:
                    index = index+1
            if y == 0 and x!= 0:
                if my_data[x,y]!= my_data[x-1,y]:
                    index = index+1
            else:
                if my_data[x,y]!= my_data[x,y-1] and my_data[x,y]!= my_data[x-1,y]:
                    index = index+1
            my_index[x,y] = index#
            old = my_data[x,y]
        if my_data[x,y] == 3 and my_data[x,y] == old:
            if x == 0 and y== 0:
                continue
            if x == 0 and y!= 0:
                if my_data[x,y]!= my_data[x,y-1]:
                    index = index+1
            if y == 0 and x!= 0:
                if my_data[x,y]!= my_data[x-1,y]:
                    index = index+1
            else:
                if my_data[x,y]!= my_data[x,y-1] and my_data[x,y]!= my_data[x-1,y]:
                    index = index+1
            my_index[x,y] = index#
            old = my_data[x,y]

#cv2.imshow("index", my_index*10)
#cv2.waitKey()
unique, counts = np.unique(my_index, return_counts=True)
print(counts)

my_map = np.zeros((height,width,3), np.uint8)
for x in range(0,height):
    for y in range(0,width):
        if my_data_2[x,y] == 2:
            my_map[x,y] = (0,0,255)
        if my_data_2[x,y] == 3:
            my_map[x,y] = (0,255,0)
        if my_data_2[x,y] == 0:
            my_map[x,y] = (100,100,100)
        if my_data_2[x,y] == -1:
            my_map[x,y] = (150,150,150)
        if my_data_2[x,y] == 1:
            my_map[x,y] = (255,255,255)

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
                    my_map[x,y] = (255,0,255)
                    x_sum = x+x_sum
                    y_sum = y+y_sum
                    n = n+1
                    if my_data[x,y] == 2:
                        is_special=True
                    else:
                        is_special=False
        print(n)
        result.append({"x":int(x_sum/n),"y":int(y_sum/n),"special":is_special})



for i in result:
    my_map[i["x"],i["y"]] = (0,0,0)

cv2.imshow("my_map",my_map)
cv2.waitKey()

#standard = 50
occupancy_level = [100, 100, 50, 30, 20, 10, 5, 1, 3, 4, 5, 1]
exit_positions_sample = [{'x': 186, 'y': 89, 'special': False}, {'x': 1, 'y': 100, 'special': False}, {'x': 137, 'y': 176, 'special': False}, {'x': 141, 'y': 108, 'special': False}, {'x': 179, 'y': 5, 'special': True}, {'x': 215, 'y': 5, 'special': True}, {'x': 236, 'y': 95, 'special': True}, {'x': 281, 'y': 171, 'special': True}, {'x': 301, 'y': 87, 'special': True}, {'x': 331, 'y': 5, 'special': True}, {'x': 351, 'y': 95, 'special': True}, {'x': 378, 'y': 89, 'special': True}]
#people_sample = [{"username": "1", "walkfast": 5, "widthrange": 5, "current_position_on_map_x": 159, "current_position_on_map_y": 80},{"username": "2", "walkfast": 5, "widthrange": 5, "current_position_on_map_x": 267, "current_position_on_map_y": 178},{"username": "3", "walkfast": 5, "widthrange": 5, "current_position_on_map_x": 184, "current_position_on_map_y": 8}]
people_sample = [{
  "_id": {
    "$oid": "6566e1514fb44d650bd63fc1"
  },
  "username": "marcel",
  "walkfast": 5,
  "climbrange": 5,
  "widthrange": 5,
  "operator": False,
  "exit_reached": False,
  "current_position_on_map_x": 26,
  "current_position_on_map_y": 41,
  "target_exit": 9
},
{
  "_id": {
    "$oid": "6566fc4300ebb422cc7bbc39"
  },
  "username": "CrookedWatch",
  "walkfast": 5,
  "climbrange": 5,
  "widthrange": 5,
  "operator": False,
  "exit_reached": False,
  "current_position_on_map_x": 354,
  "current_position_on_map_y": 122,
  "target_exit": 9
},
{
  "_id": {
    "$oid": "656701d300ebb422cc7bbc41"
  },
  "username": "BroadPurse",
  "walkfast": 5,
  "climbrange": 5,
  "widthrange": 5,
  "operator": False,
  "exit_reached": False,
  "current_position_on_map_x": 309,
  "current_position_on_map_y": 101,
  "target_exit": 3
},
{
  "_id": {
    "$oid": "65671b61877efe66d3a98bf3"
  },
  "username": "MyWatch",
  "walkfast": 5,
  "climbrange": 5,
  "widthrange": 5,
  "operator": False,
  "exit_reached": False,
  "current_position_on_map_x": 56,
  "current_position_on_map_y": 47,
  "target_exit": 5
},
{
  "_id": {
    "$oid": "65671ce075c212975ca02ddf"
  },
  "username": "User",
  "walkfast": 5,
  "climbrange": 5,
  "widthrange": 5,
  "operator": False,
  "exit_reached": False,
  "current_position_on_map_x": 75,
  "current_position_on_map_y": 37,
  "target_exit": 1
},
{
  "_id": {
    "$oid": "65671cf475c212975ca02dee"
  },
  "username": "MissUser",
  "walkfast": 5,
  "climbrange": 5,
  "widthrange": 5,
  "operator": False,
  "exit_reached": False,
  "current_position_on_map_x": 132,
  "current_position_on_map_y": 37,
  "target_exit": 3
}]
f = genfromtxt("floorplan.csv", delimiter=',')

def dijkstra(grid, start, target):
    rows, cols = len(grid), len(grid[0])
    dist = {(x, y): float('inf') for x in range(rows) for y in range(cols)}
    prev = {start: None}
    dist[start] = 0
    queue = [(0, start)]
    
    while queue:
        d, current = heapq.heappop(queue)
        if current == target:
            path = []
            while current:
                path.append(current)
                current = prev[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and dist[nx, ny] > d + 1:
                dist[nx, ny] = d + 1
                prev[(nx, ny)] = current
                heapq.heappush(queue, (d + 1, (nx, ny)))

    return []

def each_user(_user_item, _list_exits, _map):
  #print(_user_item)
  start = (_user_item["current_position_on_map_x"], _user_item["current_position_on_map_y"])
  my_map[_user_item["current_position_on_map_x"], _user_item["current_position_on_map_y"]] = (0,0,255)
  index = 0
  step = []
  pathes = []
  if _user_item["widthrange"] <= 5:
    for i in _list_exits:
      path = dijkstra(_map, start,(i["x"],i["y"]))
      pathes.append(path)
      step.append(len(path))
  else:
    for i in _list_exits:
      if i["special"] == True:
        path = dijkstra(_map, start,(i["x"],i["y"]))
        pathes.append(path)
        step.append(len(path))
      else:
        pathes.append()
        step.append(9999999)
  return pathes,step


# _people: [DBModelUser.DBModelUser]
# [{
#      },
#        "username": "CrookedWatch",
#      "walkfast": 5, # 0 (cant do nothing) -> 10 (superpower) => DISTANCE
#      "climbrange": 5, # STEPS
#      "widthrange": 5, #> WITH IF widthrange>5 => USE SPECIAL EXIT
#
#       "current_position_on_map_x": 159,
#       "current_position_on_map_y": 80,
#       "target_exit": 2 #<= NEW EXIT INDEX EXIT_LOCATIONS
#   }]
#

def compute_new_people_exit_target(_people, _exit_positions, _map) -> [int]:
  result = []
  r_p = []
  for user in _people:
    pathes,steps = each_user(user, _exit_positions, _map)
    index_min = np.argmin(steps)
    result.append(_exit_positions[index_min])
    r_p.append(pathes[index_min])
  return result,r_p

map_sample = f.tolist()
r,p = compute_new_people_exit_target(people_sample, exit_positions_sample, map_sample)
for i in r:
    my_map[i["x"],i["y"]]=(0,0,0)

cv2.imshow("my_man",my_map)
cv2.waitKey()


