from domain.image_analysis.opencv_callable.DetectPiece import *
import unittest
import numpy as np
import cv2
import os

SHOW = False

class DetectZoneDepWorldTest(unittest.TestCase):
    def setUp(self):
        print("In method ", self._testMethodName)

    def test_givenFrameOfEmbarkedCam_thenTheCorrectedPieceIsDetected(self):
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        path = os.path.normpath(os.path.join(path, os.pardir))
        # path = os.path.join(path,
        # "./image_samples/real_image/globalmonde1.jpg")

        path01 = os.path.join(path, "./samples/sampleio.jpg")
        self.call_path(path01, None, 'rouge')

        path02 = os.path.join(path, "./samples/sampleio.jpg")
        self.call_path(path02, 'carré', None)

        path1 = os.path.join(path, "./samples/sampleio1.jpg")
        self.call_path(path1, None, 'jaune')

        path2 = os.path.join(path, "./samples/sampleio2.jpg")
        self.call_path(path2, None, 'vert')

        path3 = os.path.join(path, "./samples/sampleio3.jpg")
        self.call_path(path3, None, 'bleu')

    def call_path(self, path, str_shape, str_color):
        frame = cv2.imread(path)

        if (SHOW):
          cv2.imshow('FRESH FRAME', frame)
          cv2.waitKey()

        (x, y) = detect_piece(frame, str_shape, str_color)

        if (SHOW):
          cv2.circle(frame, (x, y), 1, [255, 51, 51])
          cv2.imshow('SHAPE FRAME', frame)
          cv2.waitKey()

        self.assertNotEqual(x, 0)
        self.assertNotEqual(y, 0)

        print('Done with ', path)


if __name__ == '__main__':
    unittest.main()
