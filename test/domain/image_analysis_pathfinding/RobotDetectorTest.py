import unittest
import os
import cv2
from domain.image_path_analysis.RobotDetector import *
from domain.image_path_analysis.Exceptions.CouldNotFindRobotMarker import *


class RobotDetectorTest(unittest.TestCase):

    def setUp(self):
        self.path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.join(self.path, "./image_samples/real_image/")

    def test_given_robot_on_image_when_finding_center_of_robot_then_center_found(self):
        img = cv2.imread(self.path + "globalmonde.jpg")
        self.robot_detector = RobotDetector(img)
        x, y = self.robot_detector.find_center_of_robot()

        self.assertEqual(x, 83)
        self.assertEqual(y, 111)

    def test_given_robot_not_on_image_when_finding_center_then_ExceptionThrown(self):
        img = cv2.imread(self.path + "no_robot.png")
        self.robot_detector = RobotDetector(img)
        with self.assertRaises(CouldNotFindRobotMarkerException):
            self.robot_detector.find_center_of_robot()

    def test_given_robot_on_image_when_finding_angle_of_robot_then_angle_found(self):
        img = cv2.imread(self.path + "globalmonde.jpg")
        self.robot_detector = RobotDetector(img)
        angle = self.robot_detector.find_angle_of_robot()

