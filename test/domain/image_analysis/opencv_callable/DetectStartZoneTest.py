from domain.image_analysis.opencv_callable.DetectStartZone import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect
import time

LIVE = False
SHOW = False


class DetectStartZoneTest(unittest.TestCase):
    def setUp(self):
        print("In method ", self._testMethodName)

    def test_givenFrameOfTable_thenTheStartZoneIsDetected(self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        # path = os.path.join(path, "./image_samples/real_image/globalmonde.jpg")

        if (LIVE):
            cap = cv2.VideoCapture(1)
            ret, frame = cap.read()
            time.sleep(3)

            (x, y) = detect_start_zone(frame)

            if (SHOW):
                cv2.circle(frame, (x, y), 1, [255, 51, 51])
                cv2.imshow('SHAPE FRAME', frame)
                cv2.waitKey()

            self.assertEqual(1, 1)
        else:
            path01 = os.path.join(path, "./samples/sample1.jpg")
            self.call_path(path01)

            path1 = os.path.join(path, "./samples/sample2.jpg")
            self.call_path(path1)

            path2 = os.path.join(path, "./samples/sample3.jpg")
            self.call_path(path2)

            # path3 = os.path.join(path, "./samples/sample4.jpg")
            # self.call_path(path3)

            path4 = os.path.join(path, "./samples/sample5.jpg")
            self.call_path(path4)

            path5 = os.path.join(path, "./samples/sample6.jpg")
            self.call_path(path5)

            # path6 = os.path.join(path, "./samples/sample7.jpg")
            # self.call_path(path6)

            path7 = os.path.join(path, "./samples/sample8.jpg")
            self.call_path(path7)

            path8 = os.path.join(path, "./samples/sample9.jpg")
            self.call_path(path8)

    def call_path(self, path):
        frame = cv2.imread(path)

        if (SHOW):
            cv2.imshow('FRESH FRAME', frame)
            cv2.waitKey()

        (x, y) = detect_start_zone(frame)

        if (SHOW):
            cv2.circle(frame, (x, y), 1, [255, 51, 51])
            cv2.imshow('SHAPE FRAME', frame)
            cv2.waitKey()

        self.assertEqual(x < 170, True)
        self.assertEqual(x > 165, True)
        self.assertEqual(y < 250, True)
        self.assertEqual(y > 240, True)


if __name__ == '__main__':
    unittest.main()