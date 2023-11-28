class DBModelUser(object):
    username: str = ""
    walkfast: int = 5
    climbrange: int = 5
    widthrange: int = 5
    operator: bool = False
    exit_reached: bool = False


    def __init__(self):
        pass


    def to_json(self) -> dict:
        return {
            'username': self.username,
            'walkfast': self.walkfast,
            'climbrange': self.climbrange,
            'widthrange': self.widthrange,
            'operator': self.operator,
            'exit_reached': self.exit_reached
        }

    def __dict__(self):
        return self.to_json()
