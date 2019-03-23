from domain.image_analysis.opencv_callable.DetectPickupZone import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect


class DetectZoneDepWorldTest(unittest.TestCase):
    def setUp(self):
        print("In method ", self._testMethodName)

    def test_givenFrameOfPickupZoneWorld_thenPickupZoneIsDetected(self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))

        path1 = os.path.join(path,
                            "./image_samples/real_image/zonestart.jpg")
        shape = self.test_loop(path1)
        self.assertEqual(len(shape.shapes), 1)

        path1 = os.path.join(path,
                            "./image_samples/real_image/globalmonde.jpg")
        shape = self.test_loop(path1)
        self.assertEqual(len(shape.shapes), 1)

        path2 = os.path.join(path,
                            "./image_samples/real_image/globalmonde1.jpg")
        shape = self.test_loop(path2)
        self.assertEqual(len(shape.shapes), 1)

        path3 = os.path.join(path,
                            "./image_samples/real_image/globalmonde2.jpg")
        shape = self.test_loop(path3)
        self.assertEqual(len(shape.shapes), 1)

        path4 = os.path.join(path,
                            "./image_samples/real_image/globalmonde3.jpg")
        shape = self.test_loop(path4)
        self.assertEqual(len(shape.shapes), 1)

        path5 = os.path.join(path,
                            "./image_samples/real_image/globalmonde4.jpg")
        shape = self.test_loop(path5)

        self.assertEqual(len(shape.shapes), 1)

    def test_loop(self, path):

        frame = cv2.imread(path)

        # cap = cv2.VideoCapture(1)
        # ret, frame = cap.read()

        shape = detect_pickup_zone(frame)

        cv2.imshow('EDGES', shape.frame)
        cv2.waitKey()

        cv2.destroyAllWindows()

        return shape


if __name__ == '__main__':
    unittest.main()