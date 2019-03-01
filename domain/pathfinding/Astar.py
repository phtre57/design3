import heapq
from .Cell import Cell
from domain.image_analysis.ImageToGridConverter import *

INFINITE_WEIGHT = 9999999


class Astar(object):
    def __init__(self, grid, number_of_rows, nb_of_columns):
        self.cells = []
        self.path = []
        self.open = []
        self.visited_cells = set()
        self.starting_cell = Cell(0, 0, False)
        self.ending_cell = Cell(0, 0, False)
        self.number_of_rows = number_of_rows
        self.number_of_columns = nb_of_columns

        self.__init_cells(grid)
        self.current_cell = self.starting_cell

    def __init_cells(self, grid):
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                if grid[i][j] == EMPTY_MARKER or grid[i][j] == STARTING_MARKER:
                    reachable = True
                elif grid[i][j] == ENDING_MARKER:
                    reachable = True
                else:
                    reachable = False

                self.cells.append(Cell(i, j, reachable))

                if grid[i][j] == ENDING_MARKER:
                    self.ending_cell = self.__find_cell(i, j)

                if grid[i][j] == STARTING_MARKER:
                    self.starting_cell = self.__find_cell(i, j)

    def __calculate_cost(self, i, j):
        return abs(self.ending_cell.i - i) + abs(self.ending_cell.j - j)

    def __calculate_heuristic(self, i, j):
        return abs(i - self.ending_cell.i) + abs(j - self.ending_cell.j)

    def __find_cell(self, i, j):
        return self.cells[i * self.number_of_columns + j]

    def __set_cell(self, i, j, cell):
        self.cells[i * self.number_of_columns + j] = cell

    def __update_cell(self, selected_cell, current_cell):
        selected_cell.cost = current_cell.cost + 1
        selected_cell.heuristic = self.__calculate_heuristic(selected_cell.i, selected_cell.j)
        selected_cell.parent = current_cell
        selected_cell.net_cost = selected_cell.cost + selected_cell.heuristic

    def __rewind_path(self):
        cell = self.ending_cell
        while cell.parent is not self.starting_cell:
            self.path.append(cell)
            cell = cell.parent
        self.path.reverse()

    def __find_neighbour_cell(self):
        neighbour_cells = []

        if self.current_cell.j > 0:
            left_cell = self.__find_cell(self.current_cell.i, self.current_cell.j - 1)
            neighbour_cells.append(left_cell)

        if self.current_cell.i > 0:
            up_cell = self.__find_cell(self.current_cell.i - 1, self.current_cell.j)
            neighbour_cells.append(up_cell)

        if self.current_cell.j < self.number_of_columns - 1:
            right_cell = self.__find_cell(self.current_cell.i, self.current_cell.j + 1)
            neighbour_cells.append(right_cell)

        if self.current_cell.i < self.number_of_rows - 1:
            bottom_cell = self.__find_cell(self.current_cell.i + 1, self.current_cell.j)
            neighbour_cells.append(bottom_cell)

        return neighbour_cells

    def find_path(self):
        heapq.heapify(self.open)
        heapq.heappush(self.open, (self.starting_cell.net_cost, self.starting_cell))

        while len(self.open):
            net_cost, cell = heapq.heappop(self.open)
            self.current_cell = cell
            self.visited_cells.add(cell)

            if cell.i == self.ending_cell.i and cell.j == self.ending_cell.j:
                self.__rewind_path()
                break

            neighbours = self.__find_neighbour_cell()
            for neighbour in neighbours:
                if neighbour.reachable and neighbour not in self.visited_cells:
                    if (neighbour.net_cost, neighbour) in self.open:
                        if neighbour.cost > cell.cost + 1:
                            self.__update_cell(neighbour, cell)
                    else:
                        self.__update_cell(neighbour, cell)
                        heapq.heappush(self.open, (neighbour.net_cost, neighbour))

