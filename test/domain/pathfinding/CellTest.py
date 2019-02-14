import unittest
from domain.pathfinding.Cell import Cell


class CellTest(unittest.TestCase):

    def setUp(self):
        self.cell = Cell(1, 5, True)
        self.cell.net_cost = 50

    def test_givenTwoEqualCell_whenEquals_thenTrueReturned(self):
        self.assertEqual(self.cell, Cell(1, 5, True))

    def test_givenTwoNotEqualCellInJ_whenEquald_thenFalseReturned(self):
        self.assertNotEqual(self.cell, Cell(1, 6, True))

    def test_givenTwoNotEqualCellInI_whenEquald_thenFalseReturned(self):
        self.assertNotEqual(self.cell, Cell(8, 5, True))

    def test_givenCellHasLesserNetCost_whenLessThan_thenReturnTrue(self):
        other_cell = Cell(0, 0, True)
        other_cell.net_cost = 100
        self.assertLess(self.cell, other_cell)
