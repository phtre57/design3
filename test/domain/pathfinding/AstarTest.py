from domain.pathfinding.Astar import *
import unittest
import numpy as np


class AstarTest(unittest.TestCase):

    def setUp(self):
        print ("In method ", self._testMethodName)
        self.test2_grid = np.zeros((10, 10))
        self.test2_grid[9][9] = 3
        self.test2_grid[0][0] = 2

    def test_givenFullGridWithPathLinesAtLeftAndBottom_whenFindingPath_thenPathIsFound(self):
        for u in range(10):
            for w in range(10):
                if u != 0 and u != 9 and w != 0 and w != 9:
                    self.test2_grid[u][w] = 1

        expected_path = [Cell(0, 2, True),
                         Cell(0, 3, True),
                         Cell(0, 4, True),
                         Cell(0, 5, True),
                         Cell(0, 6, True),
                         Cell(0, 7, True),
                         Cell(0, 8, True),
                         Cell(0, 9, True),
                         Cell(1, 9, True),
                         Cell(2, 9, True),
                         Cell(3, 9, True),
                         Cell(4, 9, True),
                         Cell(5, 9, True),
                         Cell(6, 9, True),
                         Cell(7, 9, True),
                         Cell(8, 9, True),
                         Cell(9, 9, True)]

        astar = Astar(self.test2_grid, 10, 10)
        astar.find_path()
        self.assertEqual(astar.path, expected_path)

    def test_givenGridFullExceptLeftAndRightColumnsAndUpRow_whenFindingPath_thenPathFound(self):
            for u in range(10):
                for w in range(10):
                    if u != 0 and u != 10 and w != 0 and w != 10 - 1:
                        self.test2_grid[u][w] = 1

            expected_path = [Cell(0, 2, True),
                             Cell(0, 3, True),
                             Cell(0, 4, True),
                             Cell(0, 5, True),
                             Cell(0, 6, True),
                             Cell(0, 7, True),
                             Cell(0, 8, True),
                             Cell(0, 9, True),
                             Cell(1, 9, True),
                             Cell(2, 9, True),
                             Cell(3, 9, True),
                             Cell(4, 9, True),
                             Cell(5, 9, True),
                             Cell(6, 9, True),
                             Cell(7, 9, True),
                             Cell(8, 9, True),
                             Cell(9, 9, True)]

            astar = Astar(self.test2_grid, 10, 10)
            astar.find_path()
            self.assertEqual(astar.path, expected_path)


if __name__ == '__main__':
    unittest.main()