
class CouldNotFindRobotMarkerException(Exception):

    def __init__(self):
        super().__init__("Robot on marker could not be found")