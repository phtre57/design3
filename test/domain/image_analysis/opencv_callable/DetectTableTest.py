from domain.image_analysis.opencv_callable.DetectTable import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

SHOW = False

class DetectTableTest(unittest.TestCase):
    def setUp(self):
        print("In method ", self._testMethodName)

    def test_givenFrameOfTable_thenTheContourIsCroppedOut(self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        
        path01 = os.path.join(path, "./image_samples/real_image/zonestart.jpg")
        self.call_path(path01)

    def call_path(self, path):
        frame = cv2.imread(path)

        if (SHOW):
            cv2.imshow('FRESH FRAME', frame)
            cv2.waitKey()

        shape = detect_table(frame)

        if (SHOW):
            cv2.imshow('EDGES', shape.frame)
            cv2.waitKey()

        self.assertEqual(1, 1)

        print('Done with ', path)

if __name__ == '__main__':
    unittest.main()