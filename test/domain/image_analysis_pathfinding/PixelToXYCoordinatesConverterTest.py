import os
import unittest
from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from domain.pathfinding.Cell import Cell


class PixelToXYCoordinatesConverterTest(unittest.TestCase):

    def setUp(self):
        self.path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.join(self.path, "./image_samples/calibration/")
        img = cv2.imread(self.path + "calibration.png")
        self.path2 = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.path2 = os.path.normpath(os.path.join(self.path2, os.pardir))
        self.path2 = os.path.normpath(os.path.join(self.path2, os.pardir))
        self.path2 = os.path.join(self.path2, "./image_samples/piece_xy/")
        img1 = cv2.imread(self.path2 + "piece_calib_3.jpg")
        self.converter = PixelToXYCoordinatesConverter(img, 30, 7, 7, False)
        self.smallConverter = PixelToXYCoordinatesConverter(img1, 10, 4, 4, False)

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

        expected_xy_path = [(4, -8), (11, -16)]

        self.assertEqual(expected_xy_path, xy_path_temp[0:2])

    def test_realImageChessBoard(self):
        img = cv2.imread(self.path + "calib.jpg")
        converter = PixelToXYCoordinatesConverter(img, CHESS_SQUARE_WIDTH, NUMBER_OF_LINES, NUMBER_OF_COLUMNS)

    def test_givenAngle0deg_whenConvertingtoMM_thenYsignISNegative(self):
        point = (1, 4)
        real_point = self.smallConverter.convert_pixel_to_xy_point_given_angle(point, 0)
        # self.assertGreaterEqual(real_point[0], 0)
        # self.assertLessEqual(real_point[1], 0)

    def test_givenAngle90Deg_whenConvertintoMM_thenxySignIsNegative(self):
        point = (1, 4)
        real_point = self.smallConverter.convert_pixel_to_xy_point_given_angle(point, 90)
        self.assertLessEqual(real_point[0], 0)
        # self.assertLessEqual(real_point[1], 0)

    def test_givenAngle180Deg_whenConvertintoMM_thenxSignIsNegative(self):
        point = (1, 4)
        real_point = self.smallConverter.convert_pixel_to_xy_point_given_angle(point, 180)
        self.assertLessEqual(real_point[0], 0)
        self.assertGreaterEqual(real_point[1], 0)

    def test_givenAngleminus180Deg_whenConvertintoMM_thenxSignIsNegative(self):
        point = (1, 4)
        real_point = self.smallConverter.convert_pixel_to_xy_point_given_angle(point, -180)
        self.assertLessEqual(real_point[0], 0)
        self.assertGreaterEqual(real_point[1], 0)

    def test_givenAngleminus90Deg_whenConvertintoMM_thenxySignIsPositive(self):
        point = (1, 4)
        real_point = self.smallConverter.convert_pixel_to_xy_point_given_angle(point, -90)
        # self.assertGreaterEqual(real_point[0], 0)
        self.assertGreaterEqual(real_point[1], 0)




