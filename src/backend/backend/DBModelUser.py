class DBModelUser(object):
    username: str = "user"
    walkfast: int = 5
    climbrange: int = 5
    widthrange: int = 5
    operator: bool = False



    # ALGORITHM USED VARS
    exit_reached: bool = False
    current_postion_on_map_x: int = -1
    current_postion_on_map_y: int = -1
    target_exit: int = -1


    def __init__(self, _from_json_dict = None):
        _from_json_dict: dict
        if _from_json_dict is not None:
            if 'username' in _from_json_dict:
                self.username = _from_json_dict['username']
            if 'walkfast' in _from_json_dict:
                self.walkfast = _from_json_dict['walkfast']
            if 'climbrange' in _from_json_dict:
                self.climbrange = _from_json_dict['climbrange']
            if 'widthrange' in _from_json_dict:
                self.widthrange = _from_json_dict['widthrange']
            if 'operator' in _from_json_dict:
                self.operator = _from_json_dict['operator']
            if 'exit_reached' in _from_json_dict:
                self.exit_reached = _from_json_dict['exit_reached']
            if 'current_postion_on_map_x' in _from_json_dict:
                self.current_postion_on_map_x = _from_json_dict['current_postion_on_map_x']
            if 'current_postion_on_map_y' in _from_json_dict:
                self.current_postion_on_map_y = _from_json_dict['current_postion_on_map_y']
            if 'target_exit' in _from_json_dict:
                self.target_exit = _from_json_dict['target_exit']



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
