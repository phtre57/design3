class Cell(object):
    def __init__(self, x, y, reachable, end, cost):
        # setting some parameters for each cell
        self.reachable = reachable
        self.x = x
        self.y = y
        self.cost = cost
        self.end = end
        self.path = False

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self.x) + str(self.y))