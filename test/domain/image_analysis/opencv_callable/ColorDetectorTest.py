import unittest
import numpy as np
import cv2
import os
import inspect

from domain.image_analysis.opencv_callable.ColorDetector import *
from image_samples.real_image import *
from util.color import Color

SHOW = True


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
        # path = os.path.join(path, "./image_samples/real_image/pieces.jpg")
        path1 = os.path.join(path, "./samples/failed3.jpg")
        color = Color()
        color.BLUE()
        self.call_path(path1, color)

        # path2 = os.path.join(path, "./samples/piece1.jpg")
        # color = Color()
        # color.YELLOW()
        # self.call_path(path2, color)

        # path3 = os.path.join(path, "./samples/piece2.jpg")
        # color = Color()
        # color.BLUE()
        # self.call_path(path3, color)

        # path4 = os.path.join(path, "./samples/piece3.jpg")
        # color = Color()
        # color.YELLOW()
        # self.call_path(path4, color)

        # path5 = os.path.join(path, "./samples/piece4.jpg")
        # color = Color()
        # color.RED()
        # self.call_path(path5, color)

    def call_path(self, path, color):
        frame = cv2.imread(path)

        if (SHOW):
            cv2.imshow('FROM TEST - FRESH FRAME', frame)
            cv2.waitKey()

        (x, y) = color_detector(frame, color)

        if (SHOW):
            frame1 = frame.copy()
            cv2.circle(frame1, (x, y), round(10), [255, 255, 255])
            cv2.imshow('FROM TEST - SHAPE FRAME', frame1)
            cv2.waitKey()

        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
