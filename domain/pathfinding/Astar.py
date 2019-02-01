ROWS = 10
COLUMNS = 10
INFINITE_WEIGHT = 9999999;


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


class Astar(object):
    def __init__(self, grid):
        self.cells = []
        self.path = []
        self.visited_cells = set()
        self.starting_cell = 0
        self.ending_cell = 0

        for i in range(ROWS):
            for j in range(COLUMNS):
                self.cells.append(0)

        for i in range(ROWS):
            for j in range(COLUMNS):
                if grid[i][j] == 3:
                    self.ending_cell = Cell(i, j, True, True, 0)

        for i in range(ROWS):
            for j in range(COLUMNS):
                if grid[i][j] == 2:
                    self.starting_cell = Cell(i, j, True, False, self.__calculate_cost(i, j))

        self.__init_cells(grid)
        self.current_cell = self.starting_cell

    def __init_cells(self, grid):
        for i in range(ROWS):
            for j in range(COLUMNS):
                if grid[i][j] == 0 or grid[i][j] == 2:
                    reachable = True
                    end = False
                elif grid[i][j] == 3:
                    reachable = True
                    end = True
                else:
                    reachable = False
                    end = False

                cost = self.__calculate_cost(i, j)
                self.cells[i * COLUMNS + j] = Cell(i, j, reachable, end, cost)

    def __calculate_cost(self, i, j):
        return abs(self.ending_cell.x - i) + abs(self.ending_cell.y - j)

    def __calculate_heuristic(self, i, j):
        return abs(i - self.ending_cell.x) + abs(j - self.ending_cell.y)

    def __find_cell(self, i, j):
        return self.cells[i * COLUMNS + j]

    def __set_cell(self, i, j, cell):
        self.cells[i * COLUMNS + j] = cell

    def find_path(self):
        while not self.current_cell.end:
            neighbour_cell = self.find_neighbour_cell()
            heuristic = INFINITE_WEIGHT
            cost = INFINITE_WEIGHT

            for i in range(len(neighbour_cell)):
                examined_cell = neighbour_cell[i]
                calculated_heuristic = self.__calculate_heuristic(examined_cell.x, examined_cell.y)
                if examined_cell.cost <= cost and calculated_heuristic <= heuristic and examined_cell.reachable \
                        and examined_cell not in self.visited_cells:
                    heuristic = calculated_heuristic
                    next_cell = neighbour_cell[i]
                    cost = examined_cell.cost

            if next_cell.x == self.current_cell.x and next_cell.y == self.current_cell.y:
                cell = Cell(self.current_cell.x, self.current_cell.y, False, False, INFINITE_WEIGHT)
                self.__set_cell(self.current_cell.x, self.current_cell.y, cell)
                self.current_cell = self.path.pop()
                next_cell = self.current_cell
            else:
                if self.current_cell == self.starting_cell:
                    self.current_cell = next_cell
                else:
                    self.visited_cells.add(self.current_cell)
                    self.path.append(self.current_cell)
                    self.current_cell = next_cell
                    if next_cell == self.ending_cell:
                        self.path.append(next_cell)

        return self.path

    def find_neighbour_cell(self):
        neighbour_cells = []

        if self.current_cell.y > 0:
            left_cell = self.__find_cell(self.current_cell.x, self.current_cell.y - 1)
            neighbour_cells.append(left_cell)

        if self.current_cell.x > 0:
            up_cell = self.__find_cell(self.current_cell.x - 1, self.current_cell.y)
            neighbour_cells.append(up_cell)

        if self.current_cell.y < ROWS - 1:
            right_cell = self.__find_cell(self.current_cell.x, self.current_cell.y + 1)
            neighbour_cells.append(right_cell)

        if self.current_cell.x < COLUMNS - 1:
            bottom_cell = self.__find_cell(self.current_cell.x + 1, self.current_cell.y)
            neighbour_cells.append(bottom_cell)

        return neighbour_cells

    def print_cells(self):
        for i in range(ROWS):
            print("")
            for j in range(COLUMNS):
                if self.__find_cell(i, j).reachable:
                    print(self.__find_cell(i, j).cost, end=" ")
                else:
                    print("X", end=" ")

        print("")
        print("")

    def print_path(self):
        for i in range(len(self.path)):
            cell = Cell(self.path[i].x, self.path[i].y, False, False, 0)
            cell.path = True
            self.__set_cell(self.path[i].x, self.path[i].y, cell)
        for i in range(ROWS):
            print("")
            for j in range(COLUMNS):
                if self.__find_cell(i, j).path:
                    print("0", end=" ")
                elif self.__find_cell(i, j).reachable:
                    print("-", end=" ")
                else:
                    print("X", end=" ")

        print("")