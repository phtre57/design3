from domain.image_analysis.opencv_callable.DetectStartZone import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

class DetectStartZoneTest(unittest.TestCase):

    def setUp(self):
        print ("In method ", self._testMethodName)

    def test_givenFrameOfTable_thenTheStartZoneIsDetected(self):
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/globalmonde.jpg")

        frame = cv2.imread(path)

        shape = detect_start_zone(frame)
        # cv2.imshow('EDGES', shape.frame)
        # cv2.waitKey()

        self.assertEqual(shape.shapes, ['square'])

if __name__ == '__main__':
    unittest.main()