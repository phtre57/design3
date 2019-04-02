from domain.image_analysis.opencv_callable.DetectPickupZone import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

LIVE = False
SHOW = True


class DetectPickupZoneTest(unittest.TestCase):
    def setUp(self):
        print("In method ", self._testMethodName)

    def test_givenFrameOfPickupZoneWorld_thenPickupZoneIsDetected(self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        # path = os.path.join(path,
        # "./image_samples/real_image/globalmonde1.jpg")

        if (LIVE):
            cap = cv2.VideoCapture(1)
            ret, frame = cap.read()
            res = detect_pickup_zone(frame)

            cv2.circle(frame, res['point'], 1, [255, 51, 51])

            if (SHOW):
                cv2.imshow('SHAPE FRAME', frame)
                cv2.waitKey()

            self.assertNotEqual(res['point'], (0, 0))

            self.assertEqual(1, 1)
        else:
            # path01 = os.path.join(path, "./samples/sample1.jpg")
            path01 = os.path.join(path, "./testy.jpg")
            self.call_path(path01)

            path1 = os.path.join(path, "./samples/sample2.jpg")
            self.call_path(path1)

            path2 = os.path.join(path, "./samples/sample3.jpg")
            self.call_path(path2)

            path3 = os.path.join(path, "./samples/sample4.jpg")
            self.call_path(path3)

            path4 = os.path.join(path, "./samples/sample5.jpg")
            self.call_path(path4)

            path5 = os.path.join(path, "./samples/sample6.jpg")
            self.call_path(path5)

            # Flipped
            # path6 = os.path.join(path, "./samples/sample7.jpg")
            # self.call_path(path6)

            path7 = os.path.join(path, "./samples/sample8.jpg")
            self.call_path(path7)

            path8 = os.path.join(path, "./samples/sample9.jpg")
            self.call_path(path8)

            path01 = os.path.join(
                path, "./image_samples/real_image/globalmonde.jpg")
            self.call_path(path01)

            path02 = os.path.join(
                path, "./image_samples/real_image/globalmonde1.jpg")
            self.call_path(path02)

            path03 = os.path.join(
                path, "./image_samples/real_image/globalmonde2.jpg")
            self.call_path(path03)

            path04 = os.path.join(
                path, "./image_samples/real_image/globalmonde3.jpg")
            self.call_path(path04)

            path05 = os.path.join(
                path, "./image_samples/real_image/globalmonde4.jpg")
            self.call_path(path05)

            path06 = os.path.join(
                path, "./image_samples/real_image/globalmonde5.jpg")
            self.call_path(path06)

            path07 = os.path.join(
                path, "./image_samples/real_image/globalmonde6.jpg")
            self.call_path(path07)

            path08 = os.path.join(
                path, "./image_samples/real_image/globalmonde7.jpg")
            self.call_path(path08)

            path09 = os.path.join(
                path, "./image_samples/real_image/globalmonde8.jpg")
            self.call_path(path09)

            path010 = os.path.join(
                path, "./image_samples/real_image/globalmonde9.jpg")
            self.call_path(path010)

    def call_path(self, path):
        frame = cv2.imread(path)

        if (SHOW):
            cv2.imshow('FRESH FRAME', frame)
            cv2.waitKey()

        res = detect_pickup_zone(frame)

        cv2.circle(frame, res['point'], 1, [255, 51, 51])

        if (SHOW):
            cv2.imshow('SHAPE FRAME', frame)
            cv2.waitKey()

        self.assertNotEqual(res['point'][0], 0)
        self.assertNotEqual(res['point'][1], 0)

        print('Done with ', path)


if __name__ == '__main__':
    unittest.main()
