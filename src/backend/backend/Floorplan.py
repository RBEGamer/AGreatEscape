import collections
import copy
import os
import random
from pathlib import Path
import csv
import numpy
from get_center import get_center
import ai
import DBModelUser

class Floorplan:
    MAP_TILE_ID_FREE: int = 1
    MAP_TILE_ID_FREE_COLOR: str = "#bdbbbb"

    MAP_TILE_ID_BLOCKED: int = 0
    MAP_TILE_ID_BLOCKED_COLOR: str = "#7b7b7b"

    MAP_TILE_ID_EXIT_AREA: int = 3
    MAP_TILE_ID_EXIT_AREA_COLOR: str = "#4b843f"

    MAP_TILE_ID_EXIT_LOCATOR: int = 2
    MAP_TILE_ID_EXIT_LOCATOR_COLOR: str = "#90001d"

    MAP_TILE_UNITS_IN_M: float = 0.5

    BLE_BEACON_LOCATIONS: [] = []

    EXIT_CAPACITY = 10  # PEOPLE

    EXIT_LOCATIONS: [dict] = [
        {'x': 5, 'y': 142, 'special': True},  # X
        {'x': 5, 'y': 180, 'special': False},
        {'x': 5, 'y': 239, 'special': False},
        {'x': 5, 'y': 301, 'special': False},
        {'x': 5, 'y': 354, 'special': False},
        {'x': 88, 'y': 379, 'special': False},
        {'x': 171, 'y': 237, 'special': False},
        {'x': 171, 'y': 141, 'special': True},  # X
        {'x': 40, 'y': 5, 'special': True},  # X
        {'x': 150, 'y': 5, 'special': True}  # X
    ]



    RENDER_COLOR_PALETTE: [str] = []

    loaded_floorplan_matrix: numpy.ndarray = None


    def __init__(self, _map_csv_file: str = "../map/floorplan.csv"):
        floorplanfile = Path.joinpath(Path(str(os.path.dirname(os.path.realpath(__file__)))),
                                      Path(_map_csv_file)).resolve()
        print(floorplanfile)
        if not os.path.exists(floorplanfile):
            raise Exception("path invalid: {}".format(floorplanfile))

        reader = csv.reader(open(floorplanfile, "r"), delimiter=",")
        x = list(reader)
        self.loaded_floorplan_matrix = numpy.array(x).astype("int")

        print("floorplan loaded")

        # CREATE COLOR PALETTE
        self.RENDER_COLOR_PALETTE = []
        for i in range(max([self.MAP_TILE_ID_FREE, self.MAP_TILE_ID_BLOCKED, self.MAP_TILE_ID_EXIT_AREA,
                            self.MAP_TILE_ID_EXIT_LOCATOR]) + 1):
            r = lambda: random.randint(0, 255)
            self.RENDER_COLOR_PALETTE.append('#%02X%02X%02X' % (r(), r(), r()))

        self.RENDER_COLOR_PALETTE[self.MAP_TILE_ID_FREE] = self.MAP_TILE_ID_FREE_COLOR
        self.RENDER_COLOR_PALETTE[self.MAP_TILE_ID_BLOCKED] = self.MAP_TILE_ID_BLOCKED_COLOR
        self.RENDER_COLOR_PALETTE[self.MAP_TILE_ID_EXIT_AREA] = self.MAP_TILE_ID_EXIT_AREA_COLOR
        self.RENDER_COLOR_PALETTE[self.MAP_TILE_ID_EXIT_LOCATOR] = self.MAP_TILE_ID_EXIT_LOCATOR_COLOR

        self.EXIT_LOCATIONS = get_center(self.loaded_floorplan_matrix.transpose())
        self.height = self.loaded_floorplan_matrix.shape[0]
        self.width = self.loaded_floorplan_matrix.shape[1]


    def get_walking_path(self, _target: int, _x: int, _y: int):
        try:
            tex:int = self.EXIT_LOCATIONS[_target]['x']
            tey: int = self.EXIT_LOCATIONS[_target]['y']

            s = (_x, _y)
            t = (tex, tey)
            path: [] = ai.dijkstra(self.loaded_floorplan_matrix, s, t)


        except Exception as e:
            return []

    def get_user_pixeldata(self, _user: DBModelUser.DBModelUser) -> numpy.ndarray:
        if _user.target_exit < 0:
            return self.loaded_floorplan_matrix

        cx: int = _user.current_position_on_map_x
        cy: int = _user.current_position_on_map_y
        walkpath: [] = self.get_walking_path(_user.target_exit, cx, cy)


        usercpy: numpy.ndarray = copy.deepcopy(self.loaded_floorplan_matrix)

        for waypoint in walkpath:
            pass
        # TODO APPLY CUSTOM CSV WITH
        # TODO CREATE ROUTE TO APLLY THESE DATA





    def properties_to_json(self) -> dict:
        ret: dict = {
            'width': self.height,
            'height': self.width,
            'pixeldata': numpy.asarray(self.loaded_floorplan_matrix).tolist(),
            'colorpalette': self.RENDER_COLOR_PALETTE,
            'exits': self.EXIT_LOCATIONS
        }
        return ret

