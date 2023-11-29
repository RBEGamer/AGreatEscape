import DBModelUser
import Floorplan

#standard = 50
occupancy_level = [100, 100, 50, 30, 20, 10, 5, 1, 3, 4, 5, 1]
list_exits = [{'x': 186, 'y': 89, 'special': False}, {'x': 1, 'y': 100, 'special': False}, {'x': 137, 'y': 176, 'special': False}, {'x': 141, 'y': 108, 'special': False}, {'x': 179, 'y': 5, 'special': True}, {'x': 215, 'y': 5, 'special': True}, {'x': 236, 'y': 95, 'special': True}, {'x': 281, 'y': 171, 'special': True}, {'x': 301, 'y': 87, 'special': True}, {'x': 331, 'y': 5, 'special': True}, {'x': 351, 'y': 95, 'special': True}, {'x': 378, 'y': 89, 'special': True}]
list_users = [{"username": "1", "walkfast": 5, "widthrange": 5, "current_postion_on_map_x": 159, "current_postion_on_map_y": 80},{"username": "2", "walkfast": 5, "widthrange": 5, "current_postion_on_map_x": 100, "current_postion_on_map_y": 50},{"username": "3", "walkfast": 5, "widthrange": 5, "current_postion_on_map_x": 40, "current_postion_on_map_y": 30}]
my_map = genfromtxt("../map/floorplan.csv", delimiter=',')

# _people: [DBModelUser.DBModelUser]
# [{
#      },
#        "username": "CrookedWatch",
#      "walkfast": 5, # 0 (cant do nothing) -> 10 (superpower) => DISTANCE
#      "climbrange": 5, # STEPS
#      "widthrange": 5, #> WITH IF widthrange>5 => USE SPECIAL EXIT
#
#       "current_postion_on_map_x": 159,
#       "current_postion_on_map_y": 80,
#       "target_exit": 2 #<= NEW EXIT INDEX EXIT_LOCATIONS
#   }]
#
def shortestPath(self, my_map: List[List[int]], k: int) -> int:
  m = my_map.shape
  n = len(my_map[0])
  if m == 1 and n == 1:
    return 0

  dirs = [0, 1, 0, -1, 0]
  steps = 0
  q = collections.deque([(0, 0, k)])
  seen = {(0, 0, k)}

  while q:
    steps += 1
    for _ in range(len(q)):
      i, j, eliminate = q.popleft()
      for l in range(4):
        x = i + dirs[l]
        y = j + dirs[l + 1]
        if x < 0 or x == m or y < 0 or y == n:
          continue
        if x == m - 1 and y == n - 1:
          return steps
        if grid[x][y] == 1 and eliminate == 0:
          continue
        newEliminate = eliminate - grid[x][y]
        if (x, y, newEliminate) in seen:
          continue
        q.append((x, y, newEliminate))
        seen.add((x, y, newEliminate))

  return -1

def compute_new_people_exit_target(_people: [DBModelUser.DBModelUser], _exit_positions: [dict]) -> [int]:
    # _exits_position: {'x': 5, 'y': 142, 'special': True}

    pass




if __name__ == "__main__":
    f = Floorplan.Floorplan()

    compute_new_people_exit_target(_exit_positions=f.EXIT_LOCATIONS)