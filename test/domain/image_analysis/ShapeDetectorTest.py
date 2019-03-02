from domain.image_analysis.ShapeDetector import *
from domain.image_analysis.opencv_callable.Canny import canny, dilate_mask
from image_samples.real_image import *
import unittest
import numpy as np
import cv2
import os
import inspect

class DetectContourPiecesTest(unittest.TestCase):

    def setUp(self):
        self.dumb = 0

    def test_givenPiecesPicture_thenDetectTheShapeOfEveryPieces(self):
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.join(path, "./image_samples/real_image/pieces.jpg")

        frame = cv2.imread(path)

        frame = canny(frame, dilate_mask)
        shapeDetector = ShapeDetector(True, True, True)
        shapeDetector.set_peri_limiter(150, 750)
        shapeDetector.set_rect_limiter(10, 10)
        shapeDetector.set_radius_limiter(90, True)
        shape = shapeDetector.detect(frame)
        shape = shapeDetector.detect(shape.frameCnts)

        cv2.imshow('EDGES', shape.frameWithText)
        cv2.waitKey()

        self.assertEqual(shape.shapes, ['circle', 'rectangle', 'circle', 'pentagon'])

if __name__ == '__main__':
    unittest.main()