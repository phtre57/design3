class Cell(object):
    def __init__(self, i, j, reachable):
        # setting some parameters for each cell
        self.reachable = reachable
        self.i = i
        self.j = j
        self.cost = 0
        self.heuristic = 0
        self.net_cost = 0
        self.parent = None

    def __lt__(self, other):
        return self.net_cost < other.net_cost

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __hash__(self):
        return hash(str(self.i) + str(self.j))