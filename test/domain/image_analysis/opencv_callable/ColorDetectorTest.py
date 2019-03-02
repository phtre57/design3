from domain.image_analysis.opencv_callable.ColorDetector import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

class ColorDetectorTest(unittest.TestCase):

    def setUp(self):
        self.dumb = 0

    def test_givenPieces_whenColorIsGiven_thenFindTheCorrectedPiecesAssociatedToTheColor(self):
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/pieces.jpg")

        frame = cv2.imread(path)

        shape = color_detector(frame)

        cv2.imshow('EDGES', shape.frame)
        cv2.waitKey()

        self.assertEqual(shape.shapes, ['circle', 'rectangle', 'circle', 'pentagon'])

if __name__ == '__main__':
    unittest.main()