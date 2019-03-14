from domain.image_analysis.opencv_callable.DetectContourPieces import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

class DetectContourPiecesTest(unittest.TestCase):

    def setUp(self):
        print ("In method ", self._testMethodName)

    def test_givenPieces_thenTheCorrectShapeIsGivenForEveryPieces(self):
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/pieces.jpg")

        frame = cv2.imread(path)

        shape = detect_contour_pieces(frame)
        # cv2.imshow('EDGES', shape.frame)
        # cv2.waitKey()

        self.assertEqual(shape.shapes, ['circle', 'rectangle', 'circle', 'pentagon'])

if __name__ == '__main__':
    unittest.main()