from domain.image_analysis.opencv_callable.DetectZoneDep import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

class DetectZoneDepTest(unittest.TestCase):

    def setUp(self):
        self.dumb = 0

    def test_givenFrameOfZoneDep_thenZoneDepIsDetected(self):
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/zonedep.jpg")

        frame = cv2.imread(path)

        shape = detect_zone_dep(frame)
        cv2.imshow('EDGES', shape.frame)
        cv2.waitKey()

        self.assertEqual(shape.shapes, ['rectangle'])

if __name__ == '__main__':
    unittest.main()