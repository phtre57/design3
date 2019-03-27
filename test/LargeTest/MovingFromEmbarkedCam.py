import traceback
import pickle
import sys
import unittest
import os
import cv2
from domain.image_analysis.opencv_callable.DetectPiece import *

DEBUG = True

class MoveRobotWithEmbarkedCamTest(unittest.TestCase):

    def setUp(self):
        self.converter = calibrateEmbark()
        self.path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.join(self.path, "./design3/samples/")

    def test_given_east_when_finding_green_piece_then_piece_is_found(self):
        print("east")
        img = cv2.imread(self.path + "piece.jpg")
        height, width, channels = img.shape
        x, y = detect_piece(img, None, "vert")

        if DEBUG:
            cv2.circle(img, (round(width / 2), round(height / 2)), 5, [255, 255, 255])
            cv2.circle(img, (x, y), 5, [255, 255, 255])

        x = x - width/2
        y = y - height/2

        if DEBUG:
            print("In pixel :", x, y)
            print("Factors: ", self.converter.x_pixel_to_mm_factor, self.converter.y_pixel_to_mm_factor)

        real_x, real_y = self.converter.convert_pixel_to_xy_point_given_angle((x, y), 0)

        if DEBUG:
            print("Real pt: ", real_x, real_y)
            cv2.imshow("piece.jpg", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.assertGreaterEqual(real_x, 0)
        self.assertLessEqual(real_y, 0)

    def test_given_west_when_finding_green_piece_then_piece_is_found(self):
        print("west")
        img = cv2.imread(self.path + "piece.jpg")
        height, width, channels = img.shape
        x, y = detect_piece(img, None, "vert")

        if DEBUG:
            cv2.circle(img, (round(width / 2), round(height / 2)), 5, [255, 255, 255])
            cv2.circle(img, (x, y), 5, [255, 255, 255])

        x = x - width/2
        y = y - height/2

        if DEBUG:
            print("In pixel :", x, y)
            print("Factors: ", self.converter.x_pixel_to_mm_factor, self.converter.y_pixel_to_mm_factor)

        real_x, real_y = self.converter.convert_pixel_to_xy_point_given_angle((x, y), 180)

        if DEBUG:
            print("Real pt: ", real_x, real_y)
            cv2.imshow("piece.jpg", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.assertGreaterEqual(real_x, 0)
        self.assertLessEqual(real_y, 0)

    def test_given_north_when_finding_green_piece_then_piece_is_found(self):
        print("north")
        img = cv2.imread(self.path + "piece.jpg")
        height, width, channels = img.shape
        x, y = detect_piece(img, None, "vert")

        if DEBUG:
            cv2.circle(img, (round(width / 2), round(height / 2)), 5, [255, 255, 255])
            cv2.circle(img, (x, y), 5, [255, 255, 255])

        x = x - width/2
        y = y - height/2

        if DEBUG:
            print("In pixel :", x, y)
            print("Factors: ", self.converter.x_pixel_to_mm_factor, self.converter.y_pixel_to_mm_factor)

        real_x, real_y = self.converter.convert_pixel_to_xy_point_given_angle((x, y), 90)

        if DEBUG:
            print("Real pt: ", real_x, real_y)
            cv2.imshow("piece.jpg", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.assertGreaterEqual(real_x, 0)
        self.assertLessEqual(real_y, 0)

    def test_given_south_when_finding_green_piece_then_piece_is_found(self):
        print("south")
        img = cv2.imread(self.path + "piece.jpg")
        height, width, channels = img.shape
        x, y = detect_piece(img, None, "vert")

        if DEBUG:
            cv2.circle(img, (round(width / 2), round(height / 2)), 5, [255, 255, 255])
            cv2.circle(img, (x, y), 5, [255, 255, 255])

        x = x - width / 2
        y = y - height / 2

        if DEBUG:
            print("In pixel :", x, y)
            print("Factors: ", self.converter.x_pixel_to_mm_factor, self.converter.y_pixel_to_mm_factor)

        real_x, real_y = self.converter.convert_pixel_to_xy_point_given_angle((x, y), -90)

        if DEBUG:
            print("Real pt: ", real_x, real_y)
            cv2.imshow("piece.jpg", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.assertGreaterEqual(real_x, 0)
        self.assertLessEqual(real_y, 0)

    def test_given_west_when_finding_yellow_circle_piece_then_piece_is_found(self):
        print("west")
        img = cv2.imread(self.path + "piece1.jpg")
        height, width, channels = img.shape
        x, y = detect_piece(img, None, "orange")

        if DEBUG:
            cv2.circle(img, (round(width / 2), round(height / 2)), 5, [255, 255, 255])
            cv2.circle(img, (x, y), 5, [255, 255, 255])

        x = x - width / 2
        y = y - height / 2

        if DEBUG:
            print("In pixel :", x, y)
            print("Factors: ", self.converter.x_pixel_to_mm_factor, self.converter.y_pixel_to_mm_factor)

        real_x, real_y = self.converter.convert_pixel_to_xy_point_given_angle((x, y), 180)

        if DEBUG:
            print("Real pt: ", real_x, real_y)
            cv2.imshow("piece.jpg", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.assertGreaterEqual(real_x, 0)
        self.assertLessEqual(real_y, 0)

    def test_given_north_when_finding_yellow_circle_piece_then_piece_is_found(self):
        print("north")
        img = cv2.imread(self.path + "piece1.jpg")
        height, width, channels = img.shape
        x, y = detect_piece(img, None, "orange")

        if DEBUG:
            cv2.circle(img, (round(width / 2), round(height / 2)), 5, [255, 255, 255])
            cv2.circle(img, (x, y), 5, [255, 255, 255])

        x = x - width / 2
        y = y - height / 2

        if DEBUG:
            print("In pixel :", x, y)
            print("Factors: ", self.converter.x_pixel_to_mm_factor, self.converter.y_pixel_to_mm_factor)

        real_x, real_y = self.converter.convert_pixel_to_xy_point_given_angle((x, y), 180)

        if DEBUG:
            print("Real pt: ", real_x, real_y)
            cv2.imshow("piece.jpg", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.assertGreaterEqual(real_x, 0)
        self.assertLessEqual(real_y, 0)

    def test_given_north_when_finding_yellow_circle_piece9_then_piece_is_found(self):
        print("north")
        img = cv2.imread(self.path + "piece9.jpg")
        height, width, channels = img.shape
        x, y = detect_piece(img, None, "orange")

        if DEBUG:
            cv2.circle(img, (round(width / 2), round(height / 2)), 5, [255, 255, 255])
            cv2.circle(img, (x, y), 5, [255, 255, 255])

        x = x - width / 2
        y = y - height / 2

        if DEBUG:
            print("In pixel :", x, y)
            print("Factors: ", self.converter.x_pixel_to_mm_factor, self.converter.y_pixel_to_mm_factor)

        real_x, real_y = self.converter.convert_pixel_to_xy_point_given_angle((x, y), 180)

        if DEBUG:
            print("Real pt: ", real_x, real_y)
            cv2.imshow("piece9.jpg", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.assertGreaterEqual(real_x, 0)
        self.assertLessEqual(real_y, 0)

def calibrateEmbark():
    pixel_to_xy_converter = None
    try:
        with open('../../calibration_embark.pkl', 'rb') as input:
            pixel_to_xy_converter = pickle.load(input)

        return pixel_to_xy_converter
    except Exception as ex:
        print("Could not open pickle")

    return pixel_to_xy_converter
