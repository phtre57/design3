from domain.image_analysis.ShapeValidator import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

class ColorDetectorTest(unittest.TestCase):

    def setUp(self):
        print ("In method ", self._testMethodName)

    def test_givenCnts_thenDetectTheShapeAssociated(self):
        shapeValidator = ShapeValidator()
        
        self.assertEqual(shapeValidator.validate([[1], [2], [3]]), 'triangle')
        self.assertEqual(shapeValidator.validate([[1], [2], [3], [4], [5]]), 'pentagon')
        self.assertEqual(shapeValidator.validate([[1], [2], [3], [4], [5], [6]]), 'circle')

if __name__ == '__main__':
    unittest.main()