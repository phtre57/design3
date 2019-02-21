from domain.image_analysis.QR import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

class QRTest(unittest.TestCase):

    def setUp(self):
        self.dumb = 0

    def test_given_when_then(self):
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/qr.jpg")

        frame = cv2.imread(path)

        obj = decode(frame)

        self.assertEqual(str(obj.data), "b'advertising'")

if __name__ == '__main__':
    unittest.main()
