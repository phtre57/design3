import unittest
import os
from domain.image_analysis.DetectBlurriness import *


class DetectBlurrinessTest(unittest.TestCase):

    def setUp(self):
        self.path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.join(self.path, "./image_samples/blurriness/")

    def test_givenBlurryImage_whenDetectingBluriness_TrueReturned(self):
        img = cv2.imread(self.path + "blurry.jpg")
        blurriness = detect_blurriness(img)

        self.assertTrue(blurriness)

    def test_givenNonBlurryImage_whenDetectingBluriness_FalseReturned(self):
        img = cv2.imread(self.path + "non_blurry.jpg")
        blurriness = detect_blurriness(img)

        self.assertFalse(blurriness)