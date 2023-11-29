import DBModelUser
import Floorplan


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
    f = Floorplan.Floorplan()

    compute_new_people_exit_target(_exit_positions=f.EXIT_LOCATIONS)