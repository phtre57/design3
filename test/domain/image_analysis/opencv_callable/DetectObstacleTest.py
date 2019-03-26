import unittest
import os
import cv2
from domain.image_analysis.opencv_callable.DetectObstacle import *


class DetectObstacleTest(unittest.TestCase):

    def setUp(self):
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/globalmonde5.jpg")
        self.img = cv2.imread(path)
        self.img = cv2.resize(self.img, (LENGTH, HEIGHT))

    def test_givenY_whenGettingRange_thenRangeOf50PixelReturned(self):
        range_x = get_x_range(self.img, 100)
        #print(range_x)
        #cv2.imshow("test", self.img)
        #cv2.waitKey(0)

        self.assertEqual([(224, 290)], range_x)