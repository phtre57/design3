import unittest
import numpy as np
import cv2
import os
import inspect

from domain.image_analysis.opencv_callable.ColorDetector import *
from image_samples.real_image import *
from util.color import Color


class ColorDetectorTest(unittest.TestCase):
    def setUp(self):
        print("In method ", self._testMethodName)

    def test_givenPieces_whenColorIsGiven_thenFindTheCorrectedPiecesAssociatedToYELLOW(
            self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/pieces.jpg")

        frame = cv2.imread(path)

        color = Color()
        color.YELLOW()
        shape = color_detector(frame, color)

        # cv2.imshow('EDGES', shape.res_contour[3])
        # cv2.waitKey()

        self.assertEqual(shape.shapes,
                         ['circle', 'rectangle', 'circle', 'pentagon'])

    def test_givenPieces_whenColorIsGiven_thenFindTheCorrectedPiecesAssociatedToRED(
            self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/pieces.jpg")

        frame = cv2.imread(path)

        color = Color()
        color.RED()
        shape = color_detector(frame, color)

        # cv2.imshow('EDGES', shape.frame)
        # cv2.imshow('EDGES', shape.res_contour[3])
        # cv2.waitKey()

        self.assertEqual(shape.shapes,
                         ['circle', 'rectangle', 'circle', 'pentagon'])

    def test_givenPieces_whenColorIsGiven_thenFindTheCorrectedPiecesAssociatedToBLUE(
            self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/pieces.jpg")

        frame = cv2.imread(path)

        color = Color()
        color.BLUE()
        shape = color_detector(frame, color)

        # cv2.imshow('EDGES', shape.frame)
        # cv2.imshow('EDGES', shape.res_contour[3])
        # cv2.waitKey()

        self.assertEqual(shape.shapes,
                         ['circle', 'rectangle', 'circle', 'pentagon'])

    def test_givenPieces_whenColorIsGiven_thenFindTheCorrectedPiecesAssociatedToGREEN(
            self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/pieces1.jpg")

        frame = cv2.imread(path)

        color = Color()
        color.GREEN()
        shape = color_detector(frame, color)

        # cv2.imshow('EDGES', shape.frame)
        # cv2.imshow('EDGES', shape.res_contour[3])
        # cv2.waitKey()

        # self.assertEqual(shape.shapes,
        #  ['circle', 'rectangle', 'circle', 'pentagon'])

    def test_givenPieces_whenColorIsGiven_thenFindTheCorrectedPiecesAssociatedToTEST(
            self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/pieces1.jpg")

        frame = cv2.imread(path)

        color = Color()
        color.GREEN()
        shape = color_detector(frame, color)

        # print(shape.res_contour[0])

        # cv2.circle(shape.res_contour[3], shape.res_contour[2], int(3), [0,0,255], 2)

        # print(shape.res_contour[1])

        # # cv2.imshow('EDGES', shape.frame)
        # cv2.imshow('EDGES', shape.res_contour[3])
        # cv2.waitKey()

        # self.assertEqual(shape.shapes, ['circle', 'rectangle', 'circle', 'pentagon'])


if __name__ == '__main__':
    unittest.main()
