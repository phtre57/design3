from domain.image_analysis.opencv_callable.DetectZoneDepWorld import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

class DetectZoneDepWorldTest(unittest.TestCase):

    def setUp(self):
        print ("In method ", self._testMethodName)

    def test_givenFrameOfZoneDepWorld_thenZoneDepIsDetected(self):
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/globalmonde10.jpg")

        frame = cv2.imread(path)

        # cap = cv2.VideoCapture(1)
        # ret, frame = cap.read()

        shape = detect_zone_dep_world(frame)

        cv2.imshow('EDGES', shape.frame)
        cv2.waitKey()

        self.assertEqual(shape.shapes, ['rectangle'])

if __name__ == '__main__':
    unittest.main()