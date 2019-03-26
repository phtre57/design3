class NoBeginingPointException(Exception):
    def __init__(self):
        super().__init__("No begin point for Astar")