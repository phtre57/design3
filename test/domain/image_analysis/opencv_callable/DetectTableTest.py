from domain.image_analysis.opencv_callable.DetectTable import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect


class DetectTableTest(unittest.TestCase):
    def setUp(self):
        print("In method ", self._testMethodName)

    def test_givenFrameOfTable_thenTheContourIsCroppedOut(self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/zonestart.jpg")

        frame = cv2.imread(path)

        shape = detect_table(frame)
        cv2.imshow('EDGES', shape.frame)
        cv2.waitKey()

        self.assertEqual(shape.shapes, ['rectangle'])


if __name__ == '__main__':
    unittest.main()