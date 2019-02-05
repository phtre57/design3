from domain.pathfinding.Astar import *
import unittest
import numpy as np


class AstarTest(unittest.TestCase):

    def setUp(self):
        self.test2_grid = np.zeros((10, 10))
        self.test2_grid[9][9] = 3
        self.test2_grid[0][0] = 2


    def test_givenFullGridWithPathLinesAtLeftAndBottom_whenFindingPath_thenPathIsFound(self):
        for u in range(10):
            for w in range(10):
                if u != 0 and u != 9 and w != 0 and w != 9:
                    self.test2_grid[u][w] = 1

        expected_path = [Cell(1, 0, True, False, 17),
                         Cell(2, 0, True, False, 16),
                         Cell(3, 0 , True, False, 15),
                         Cell(4, 0, True, False, 14),
                         Cell(5, 0, True, False, 13),
                         Cell(6, 0, True, False, 12),
                         Cell(7, 0, True, False, 11),
                         Cell(8, 0, True, False, 10),
                         Cell(9, 0, True, False, 9),
                         Cell(9, 1, True, False, 8),
                         Cell(9, 2, True, False, 7),
                         Cell(9, 3, True, False, 6),
                         Cell(9, 4, True, False, 5),
                         Cell(9, 5, True, False, 4),
                         Cell(9, 6, True, False, 3),
                         Cell(9, 7, True, False, 2),
                         Cell(9, 8, True, False, 1),
                         Cell(9, 9, True, True, 0)]

        astar = Astar(self.test2_grid, 10, 10)
        astar.find_path()
        self.assertEqual(astar.path, expected_path)

    def test_givenGridFullExceptLeftAndRightColumnsAndUpRow_whenFindingPath_thenPathFound(self):
            for u in range(10):
                for w in range(10):
                    if u != 0 and u != 10 and w != 0 and w != 10 - 1:
                        self.test2_grid[u][w] = 1

            expected_path = [Cell(0, 1, True, False, 17),
                             Cell(0, 2, True, False, 16),
                             Cell(0, 3, True, False, 15),
                             Cell(0, 4, True, False, 14),
                             Cell(0, 5, True, False, 13),
                             Cell(0, 6, True, False, 12),
                             Cell(0, 7, True, False, 11),
                             Cell(0, 8, True, False, 10),
                             Cell(0, 9, True, False, 9),
                             Cell(1, 9, True, False, 8),
                             Cell(2, 9, True, False, 7),
                             Cell(3, 9, True, False, 6),
                             Cell(4, 9, True, False, 5),
                             Cell(5, 9, True, False, 4),
                             Cell(6, 9, True, False, 3),
                             Cell(7, 9, True, False, 2),
                             Cell(8, 9, True, False, 1),
                             Cell(9, 9, True, True, 0)]

            astar = Astar(self.test2_grid, 10, 10)
            astar.find_path()
            self.assertEqual(astar.path, expected_path)


if __name__ == '__main__':
    unittest.main()