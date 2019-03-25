from domain.image_analysis.opencv_callable.DetectStartZone import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect
import time


class DetectStartZoneTest(unittest.TestCase):
    def setUp(self):
        print("In method ", self._testMethodName)

    def test_givenFrameOfTable_thenTheStartZoneIsDetected(self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/globalmonde.jpg")

        frame = cv2.imread(path)

        cap = cv2.VideoCapture(1)
        time.sleep(1)
        _, frame = cap.read()

        shape = detect_start_zone(frame)

        cv2.imshow('EDGES', shape.frame)
        cv2.waitKey()

        cv2.circle(shape.frame, (shape.center[0], shape.center[1]), 1,
                   [255, 51, 51])

        cv2.imshow('CENTER', shape.frame)
        cv2.waitKey()

        self.assertEqual(shape.shapes, ['square'])


if __name__ == '__main__':
    unittest.main()