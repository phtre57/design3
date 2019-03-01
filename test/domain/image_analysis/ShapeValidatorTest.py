from domain.image_analysis.ShapeValidator import *
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

class ColorDetectorTest(unittest.TestCase):

    def setUp(self):
        self.dumb = 0

    def test_given_when_then(self):
        shapeValidator = ShapeValidator()
        
        self.assertEqual(shapeValidator.validate([[1], [2], [3]]), 'triangle')
        self.assertEqual(shapeValidator.validate([[1], [2], [3], [4], [5]]), 'pentagon')
        self.assertEqual(shapeValidator.validate([[1], [2], [3], [4], [5], [6]]), 'circle')

if __name__ == '__main__':
    unittest.main()