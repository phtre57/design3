from domain.image_analysis.opencv_callable.DetectContourPieces import *
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

        path001 = os.path.join(path, "./test.jpg")
        # path001 = os.path.join(path, "./samples/HD/shapes.jpg")
        str_shape = 'pentagone'
        self.call_path(path001, str_shape)

        path01 = os.path.join(path, "./samples/HD/shapes.jpg")
        str_shape = 'pentagone'
        self.call_path(path01, str_shape)

        path01 = os.path.join(path, "./samples/HD/shapes1.jpg")
        str_shape = 'cercle'
        self.call_path(path01, str_shape)

        path01 = os.path.join(path, "./samples/HD/shapes1.jpg")
        str_shape = 'triangle'
        self.call_path(path01, str_shape)

        path01 = os.path.join(path, "./samples/HD/shapes2.jpg")
        str_shape = 'cercle'
        self.call_path(path01, str_shape)

        path01 = os.path.join(path, "./samples/HD/pentagon2.jpg")
        str_shape = 'pentagone'
        self.call_path(path01, str_shape)

        path01 = os.path.join(path, "./samples/HD/triangle1.jpg")
        str_shape = 'triangle'
        self.call_path(path01, str_shape)

        path01 = os.path.join(path, "./samples/HD/shapes2.jpg")
        str_shape = 'carré'
        self.call_path(path01, str_shape)

        path01 = os.path.join(path, "./samples/HD/shapes3.jpg")
        str_shape = 'cercle'
        self.call_path(path01, str_shape)

        path01 = os.path.join(path, "./samples/HD/shapes3.jpg")
        str_shape = 'pentagone'
        self.call_path(path01, str_shape)

        path01 = os.path.join(path, "./samples/HD/circle.jpg")
        str_shape = 'cercle'
        self.call_path(path01, str_shape)

        path01 = os.path.join(path, "./samples/HD/square.jpg")
        str_shape = 'carré'
        self.call_path(path01, str_shape)

        path01 = os.path.join(path, "./samples/HD/triangle.jpg")
        str_shape = 'triangle'
        self.call_path(path01, str_shape)

        path1 = os.path.join(path, "./samples/HD/trianglej.jpg")
        str_shape = 'triangle'
        self.call_path(path1, str_shape)

        path2 = os.path.join(path, "./samples/HD/pentagon.jpg")
        str_shape = 'pentagone'
        self.call_path(path2, str_shape)

    def call_path(self, path, str_shape):
        frame = cv2.imread(path)

        if (SHOW):
            cv2.imshow('FROM TEST - FRESH FRAME', frame)
            cv2.waitKey()

        (x, y) = detect_contour_pieces(frame, str_shape)

        if (SHOW):
            cv2.circle(frame, (x * 5, y * 5), 20, [0, 110, 110])
            cv2.imshow('FROM TEST - SHAPE FRAME', frame)
            cv2.waitKey()

        self.assertNotEqual(x, 0)
        self.assertNotEqual(y, 0)


if __name__ == '__main__':
    unittest.main()