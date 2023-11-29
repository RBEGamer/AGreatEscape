import os
import random
from pathlib import Path
import csv
import numpy
import get_center



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



    BLE_BEACON_LOCATIONS: [] = [

    ]


    EXIT_LOCATIONS: [] = get_center("../map/floorplan.csv")
    #EXIT_LOCATIONS: [] = [
    #    {'x': 5, 'y': 142, 'special': True},  # X
    #    {'x': 5, 'y': 180, 'special': False},
    #    {'x': 5, 'y': 239, 'special': False},
    #    {'x': 5, 'y': 301, 'special': False},
    #    {'x': 5, 'y': 354, 'special': False},
    #    {'x': 88, 'y': 379, 'special': False},
    #    {'x': 171, 'y': 237, 'special': False},
    #    {'x': 171, 'y': 141, 'special': True},  # X
    #    {'x': 40, 'y': 5, 'special': True},  # X
        {'x': 150, 'y': 5, 'special': True}  # X

    ]


    RENDER_COLOR_PALETTE: [str] = []

    loaded_floorplan_matrix: numpy.ndarray = None

    def __init__(self, _map_csv_file:str = "../map/floorplan.csv"):
        floorplanfile = Path.joinpath(Path(str(os.path.dirname(os.path.realpath(__file__)))), Path(_map_csv_file)).resolve()
        print(floorplanfile)
        if not os.path.exists(floorplanfile):
            raise Exception("path invalid: {}".format(floorplanfile))


        reader = csv.reader(open(floorplanfile, "r"), delimiter=",")
        x = list(reader)
        self.loaded_floorplan_matrix = numpy.array(x).astype("int").transpose()

        print("floorplan loaded")


        # CREATE COLOR PALETTE
        self.RENDER_COLOR_PALETTE = []
        for i in range(max([self.MAP_TILE_ID_FREE, self.MAP_TILE_ID_BLOCKED, self.MAP_TILE_ID_EXIT_AREA, self.MAP_TILE_ID_EXIT_LOCATOR])+1):
            r = lambda: random.randint(0, 255)
            self.RENDER_COLOR_PALETTE.append('#%02X%02X%02X' % (r(), r(), r()))

        self.RENDER_COLOR_PALETTE[self.MAP_TILE_ID_FREE] = self.MAP_TILE_ID_FREE_COLOR
        self.RENDER_COLOR_PALETTE[self.MAP_TILE_ID_BLOCKED] = self.MAP_TILE_ID_BLOCKED_COLOR
        self.RENDER_COLOR_PALETTE[self.MAP_TILE_ID_EXIT_AREA] = self.MAP_TILE_ID_EXIT_AREA_COLOR
        self.RENDER_COLOR_PALETTE[self.MAP_TILE_ID_EXIT_LOCATOR] = self.MAP_TILE_ID_EXIT_LOCATOR_COLOR


    def properties_to_json(self) -> dict:
        ret:dict = {
            'width': 180,
            'height': 380,
            'pixeldata': numpy.asarray(self.loaded_floorplan_matrix.transpose()).tolist(),
            'colorpalette': self.RENDER_COLOR_PALETTE,
            'exits': self.EXIT_LOCATIONS
        }
        return ret