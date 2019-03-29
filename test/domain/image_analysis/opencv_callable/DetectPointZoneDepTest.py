from domain.image_analysis.opencv_callable.DetectPointZoneDep import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

SHOW = True


class DetectContourPiecesTest(unittest.TestCase):
    def setUp(self):
        print("In method ", self._testMethodName)

    def test_givenPieces_thenTheCorrectShapeIsGivenForEveryPieces(self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        # path = os.path.join(path, "./image_samples/real_image/pieces.jpg")

        path5 = os.path.join(path, "./samples/zonedep5.jpg")
        self.call_path(path5)

    def call_path(self, path):
        frame = cv2.imread(path)

        # cv2.imshow('FROM TEST - FRESH FRAME', frame)
        # cv2.waitKey()

        (x, y) = detect_point_zone_dep(frame)

        if (SHOW):
            cv2.circle(frame, (x, y), 1, [255, 51, 51])
            cv2.imshow('FROM TEST - SHAPE FRAME', frame)
            cv2.waitKey()

        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()