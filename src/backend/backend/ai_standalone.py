import DBModelUser
import Floorplan
import numpy as np
from numpy import genfromtxt
import heapq


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
f = genfromtxt("../map/floorplan.csv", delimiter=',')

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
  index = 0
  step = []
  if _user_item["widthrange"] <= 5:
    for i in _list_exits:
      path = dijkstra(_map, start,(i["x"],i["y"]))
      step.append(len(path))
  else:
    for i in _list_exits:
      if i["special"] == True:
        path = dijkstra(_map, start,(i["x"],i["y"]))
        step.append(len(path))
      else:
        step.append(9999999)
  return(step)


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
  for user in _people:
    steps = each_user(user, _exit_positions, _map)
    index_min = np.argmin(steps)
    result.append(_exit_positions[index_min])
  return result

if __name__ == "__main__":
  #f = Floorplan.Floorplan()
  map_sample = f.tolist()
  print(compute_new_people_exit_target(people_sample, exit_positions_sample, map_sample))