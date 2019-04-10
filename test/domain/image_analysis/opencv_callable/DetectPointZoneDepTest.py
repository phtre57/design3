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

    def test_givenZoneDep_thenTheNearestPointIsDetected(self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        # path = os.path.join(path, "./image_samples/real_image/pieces.jpg")

        # path1 = os.path.join(path, "./samples/zonedep4.jpg")
        path1 = os.path.join(path, "./test.jpg")
        self.call_path(path1)

        path2 = os.path.join(path, "./samples/zonedep5.jpg")
        self.call_path(path2)

        path3 = os.path.join(path, "./samples/zonedep2.jpg")
        self.call_path(path3)

        path4 = os.path.join(path, "./samples/zonedep7.jpg")
        self.call_path(path4)

        path5 = os.path.join(path, "./samples/zonedep8.jpg")
        self.call_path(path5)

        path6 = os.path.join(path, "./samples/zonedep9.jpg")
        self.call_path(path6)

    def call_path(self, path):
        frame = cv2.imread(path)

        # cv2.imshow('FROM TEST - FRESH FRAME', frame)
        # cv2.waitKey()

        (x, y) = detect_point_zone_dep(frame)

        if (SHOW):
            cv2.circle(frame, (x, y), 5, [255, 51, 51])
            cv2.imshow('FROM TEST - SHAPE FRAME', frame)
            cv2.waitKey()

        # Validation que ce qui est trouvé n'est pas bidon
        self.assertNotEqual(x, 0)
        self.assertNotEqual(y, 0)


if __name__ == '__main__':
    unittest.main()