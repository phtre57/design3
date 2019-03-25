from domain.image_analysis.opencv_callable.DetectQR import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect
from domain.QRCodeDictionnary import *

class QRTest(unittest.TestCase):

    def setUp(self):
        print ("In method ", self._testMethodName)

    def test_givenQRCode_thenItIsCorrectlyDecoded(self):
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/qr.png")

        frame = cv2.imread(path)

        obj = decode(frame)

        self.assertEqual(obj[COULEUR], "rouge")
        self.assertEqual(obj[PIECE], None)
        self.assertEqual(obj[ZONE], "Zone 0")


if __name__ == '__main__':
    unittest.main()
