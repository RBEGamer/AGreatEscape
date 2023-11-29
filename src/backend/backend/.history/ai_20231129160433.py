import DBModelUser
import Floorplan

#standard = 50
occupancy_level = [100, 100, 50, 30, 20, 10, 5, 1, 3, 4, 5, 1]
list_exits = [{'x': 186, 'y': 89, 'special': False}, {'x': 1, 'y': 100, 'special': False}, {'x': 137, 'y': 176, 'special': False}, {'x': 141, 'y': 108, 'special': False}, {'x': 179, 'y': 5, 'special': True}, {'x': 215, 'y': 5, 'special': True}, {'x': 236, 'y': 95, 'special': True}, {'x': 281, 'y': 171, 'special': True}, {'x': 301, 'y': 87, 'special': True}, {'x': 331, 'y': 5, 'special': True}, {'x': 351, 'y': 95, 'special': True}, {'x': 378, 'y': 89, 'special': True}]
list_users = [{"username": "1", "walkfast": 5, "widthrange": 5, "current_postion_on_map_x": 159, "current_postion_on_map_y": 80},{"username": "2", "walkfast": 5, "widthrange": 5, "current_postion_on_map_x": 100, "current_postion_on_map_y": 50},{"username": "3", "walkfast": 5, "widthrange": 5, "current_postion_on_map_x": 40, "current_postion_on_map_y": 30}]
my_map = genfromtxt("../map/floorplan.csv", delimiter=',')


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

list_my_map = my_map.tolist()
print(path = dijkstra(list_my_map, (159,80),(186,89)))

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

def compute_new_people_exit_target(_people: [DBModelUser.DBModelUser], _exit_positions: [dict]) -> [int]:
    # _exits_position: {'x': 5, 'y': 142, 'special': True}
    pass




if __name__ == "__main__":

  list_my_map = 
    f = Floorplan.Floorplan()

    compute_new_people_exit_target(_exit_positions=f.EXIT_LOCATIONS)