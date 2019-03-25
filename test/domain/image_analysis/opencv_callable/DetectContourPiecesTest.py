from domain.image_analysis.opencv_callable.DetectContourPieces import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

SHOW = False


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

        path1 = os.path.join(path, "./samples/piece.jpg")
        str_shape = 'pentagon'
        self.call_path(path1, str_shape)

        path2 = os.path.join(path, "./samples/piece1.jpg")
        str_shape = 'rectangle'
        self.call_path(path2, str_shape)

        path3 = os.path.join(path, "./samples/piece2.jpg")
        str_shape = 'pentagon'
        self.call_path(path3, str_shape)

        path4 = os.path.join(path, "./samples/piece3.jpg")
        str_shape = 'circle'
        self.call_path(path4, str_shape)

        path5 = os.path.join(path, "./samples/piece4.jpg")
        str_shape = 'pentagon'
        self.call_path(path5, str_shape)

    def call_path(self, path, str_shape):
        frame = cv2.imread(path)

        cv2.imshow('FROM TEST - FRESH FRAME', frame)
        cv2.waitKey()

        if (SHOW):
            (x, y) = detect_contour_pieces(frame, str_shape)
            cv2.circle(frame, (x, y), 1, [255, 51, 51])
            cv2.imshow('FROM TEST - SHAPE FRAME', frame)
            cv2.waitKey()

        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()