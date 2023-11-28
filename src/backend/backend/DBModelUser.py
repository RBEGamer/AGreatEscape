class DBModelUser(object):
    username: str = ""
    walkfast: int = 5
    climbrange: int = 5
    widthrange: int = 5
    operator: bool = False



    # ALGORITHM USED VARS
    exit_reached: bool = False
    current_postion_on_map_x: int = -1
    current_postion_on_map_y: int = -1
    target_exit: int = -1


    def __init__(self):
        pass


    def to_json(self) -> dict:
        return {
            'username': self.username,
            'walkfast': self.walkfast,
            'climbrange': self.climbrange,
            'widthrange': self.widthrange,
            'operator': self.operator,
            'exit_reached': self.exit_reached,
            'current_postion_on_map_x': self.current_postion_on_map_x,
            'current_postion_on_map_y': self.current_postion_on_map_y,
            'target_exit': self.target_exit
        }

    def __dict__(self):
        return self.to_json()
