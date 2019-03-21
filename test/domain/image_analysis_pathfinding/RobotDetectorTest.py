import unittest
import os
import cv2
from domain.image_analysis_pathfinding.RobotDetector import *
from domain.image_analysis.Exceptions.CouldNotFindRobotMarker import *


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

        self.assertEqual(x, 84)
        self.assertEqual(y, 111)

    def test_given_robot_not_on_image_when_finding_center_then_ExceptionThrown(self):
        img = cv2.imread(self.path + "no_robot.png")
        self.robot_detector = RobotDetector(img)
        with self.assertRaises(CouldNotFindRobotMarkerException):
            self.robot_detector.find_center_of_robot()

    def test_given_robot_on_image_withAngle_near40degrees_when_finding_angle_of_robot_then_angle_found_is07radian(self):
        img = cv2.imread(self.path + "globalmonde.jpg")
        self.robot_detector = RobotDetector(img)
        angle = self.robot_detector.find_angle_of_robot()

        self.assertGreaterEqual(angle, 40)
        self.assertLessEqual(angle, 45)

    def test_given_robot_on_image_with_angle_minus40degrees_when_finding_angle_thenAngle_found_isminus_06radian(self):
        img = cv2.imread(self.path + "globalmonde2.jpg")
        self.robot_detector = RobotDetector(img)
        angle = self.robot_detector.find_angle_of_robot()

        self.assertLessEqual(angle, -30)
        self.assertGreaterEqual(angle, -36)

    def test_given_robot_on_image_with_angle_minus140degrees_when_finding_angle_thenAngle_found_isminus_06radian(self):
        img = cv2.imread(self.path + "globalmonde6.jpg")
        self.robot_detector = RobotDetector(img)
        angle = self.robot_detector.find_angle_of_robot()

        self.assertGreaterEqual(angle, 130)
        self.assertLessEqual(angle, 145)
