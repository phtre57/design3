import cv2
import math
import numpy as np
from domain.image_analysis.ImageToGridConverter import LENGTH, HEIGHT
from domain.image_analysis.Exceptions.CouldNotFindRobotMarker import *

YELLOW_HSV_LOW = np.array([20, 100, 160])
YELLOW_HSV_HIGH = np.array([30, 255, 255])
RED_HSV_LOW = np.array([150, 100, 100])
RED_HSV_HIGH = hsv_high = np.array([180, 255, 255])
RADIUS_OF_MARKER = 5

debug = False


class RobotDetector:
    def __init__(self, image):
        self.image = image.copy()
        self.image = cv2.resize(self.image, (LENGTH, HEIGHT))

    def find_center_of_robot(self):
        yellow_x_center_of_contour, yellow_y_center_of_contour = self.__find_yellow_marker_center(
        )
        red_x_center_of_contour, red_y_center_of_contour = self.__find_red_marker_center(
        )

        half_distance_between_x = round(
            abs(yellow_x_center_of_contour - red_x_center_of_contour) / 2)
        half_distance_between_y = round(
            abs(yellow_y_center_of_contour - red_y_center_of_contour) / 2)

        if red_x_center_of_contour < yellow_x_center_of_contour:
            x_starting_pt = red_x_center_of_contour + half_distance_between_x
        else:
            x_starting_pt = yellow_x_center_of_contour + half_distance_between_x

        if red_y_center_of_contour < yellow_y_center_of_contour:
            y_starting_pt = red_y_center_of_contour + half_distance_between_y
        else:
            y_starting_pt = yellow_y_center_of_contour + half_distance_between_y

        if debug:
            print(x_starting_pt, y_starting_pt)
            cv2.imshow("robot detector", self.image)

        return x_starting_pt, y_starting_pt

    def find_angle_of_robot(self):
        yellow_x_center_of_contour, yellow_y_center_of_contour = self.__find_yellow_marker_center(
        )
        red_x_center_of_contour, red_y_center_of_contour = self.__find_red_marker_center(
        )

        vector = (yellow_x_center_of_contour - red_x_center_of_contour,
                  yellow_y_center_of_contour - red_y_center_of_contour)

        angle = math.atan2(vector[1], vector[0])

        # WIP NEED TEST
        return math.degrees(
            angle) * -1  # we change sign here to fit with robot referential

    def __find_center_of_contour(self, mask):
        ret, thresh = cv2.threshold(mask, 60, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)

            try:
                if radius >= RADIUS_OF_MARKER:
                    M = cv2.moments(contour)
                    x_center_of_contour = int(M["m10"] / M["m00"])
                    y_center_of_contour = int(M["m01"] / M["m00"])
                    return x_center_of_contour, y_center_of_contour

            except ZeroDivisionError:
                raise CouldNotFindRobotMarkerException()

        raise CouldNotFindRobotMarkerException()

    def __find_yellow_marker_center(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, YELLOW_HSV_LOW, YELLOW_HSV_HIGH)

        kernelerode = np.ones((2, 2), np.uint8)
        mask = cv2.erode(mask, kernelerode, iterations=1)

        if (debug):
            cv2.imshow("yellow_mask", mask)
            cv2.waitKey(0)
        return self.__find_center_of_contour(mask)

    def __find_red_marker_center(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, RED_HSV_LOW, RED_HSV_HIGH)

        kernelerode = np.ones((2, 2), np.uint8)
        mask = cv2.erode(mask, kernelerode, iterations=1)

        if (debug):
            cv2.imshow("red_mask", mask)
            cv2.waitKey(0)
        return self.__find_center_of_contour(mask)