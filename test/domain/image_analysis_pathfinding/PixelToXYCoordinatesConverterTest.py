import os
import unittest
from domain.image_path_analysis.PixelToXYCoordinatesConverter import *
from domain.pathfinding.Cell import Cell


class PixelToXYCoordinatesConverterTest(unittest.TestCase):

    def setUp(self):
        self.path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.join(self.path, "./image_samples/calibration/")
        self.converter = PixelToXYCoordinatesConverter(self.path + "calibration.png", 30, 7, 7)

    def test_givenChessBoardWith16PixelBetweenSquareInX_thenWidthCalculatedIs16(self):
        self.assertEqual(round(self.converter.x_pixel_square_width), 16)

    def test_givenChessBoardWith15PixelBetweenSquareInY_thenHeigthCalculatedIs15(self):
        self.assertEqual(round(self.converter.y_pixel_square_width), 15)

    def test_givenChessBoardWith15PixelBetweenSquareInY_thenFactorCalculatedIs2(self):
        self.assertEqual(round(self.converter.y_pixel_to_mm_factor), 2)

    def test_givenChessBoardWith15PixelBetweenSquareInX_thenFactorCalculatedIs2(self):
        self.assertEqual(round(self.converter.x_pixel_to_mm_factor), 2)

    def test_givenArrayContainingCell_whenConvertingToXYCoord_thenIsMultipliedByAFactorOf2(self):
        path = [(1, 2), (3, 4)]
        xy_path = self.converter.convert_to_xy(path)
        xy_path_temp = []
        for tuple in xy_path:
            xy_path_temp.append((round(tuple[0]), round(tuple[1])))

        expected_xy_path = [(2, -4), (6, -8)]

        self.assertEqual(expected_xy_path, xy_path_temp)

    def test_(self):
        converter = PixelToXYCoordinatesConverter(self.path + "calib2.jpg", CHESS_SQUARE_WIDTH, NUMBER_OF_LINES, NUMBER_OF_COLUMNS)



