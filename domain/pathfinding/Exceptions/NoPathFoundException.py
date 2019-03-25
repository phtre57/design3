class NoPathFoundException(Exception):
    def __init__(self):
        super().__init__("No path was found for end point")