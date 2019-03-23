class NoPathFoundException(Exception):

    def __init__(self):
        super().__init__("No path wa found for end point")