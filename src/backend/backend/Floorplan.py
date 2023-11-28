import os
from pathlib import Path
import csv
import numpy



class Floorplan:


    MAP_TILE_ID_FREE: int = 1
    MAP_TILE_ID_BLOCKED: int = 0
    MAP_TILE_ID_EXIT_AREA: int = 3
    MAP_TILE_ID_EXIT_LOCATOR: int = 2

    MAP_TILE_UNITS_IN_M: float = 0.5


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


    def properties_to_json(self) -> dict:
        return {
            'width': 180,
            'height': 380
        }