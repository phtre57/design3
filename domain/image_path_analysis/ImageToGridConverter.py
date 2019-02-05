import numpy as np
import sys
import cv2
np.set_printoptions(threshold=sys.maxsize)

LENGTH = 640
WIDTH = 400

OBSTACLE_MARKER = 1
EMPTY_MARKER = 0
STARTING_MARKER = 2
ENDING_MARKER = 3
HSV_IN_RANGE_MARKER = 255


class ImageToGridConverter(object):
    def __init__(self, image):
        self.image = image
        self.image = cv2.resize(self.image, (LENGTH, WIDTH))
        self.grid = np.zeros((WIDTH, LENGTH))
        self.mark_starting_point()
        self.mark_ending_point()
        self.mark_obstacle_in_grid_from_image()

    def mark_obstacle_in_grid_from_image(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        #hsv for blue
        hsv_low = np.array([100, 150, 0])
        hsv_high = np.array([140, 255, 255])

        mask = cv2.inRange(hsv, hsv_low, hsv_high)
        for i in range(WIDTH):
            for j in range(LENGTH):
                if mask[i][j] == HSV_IN_RANGE_MARKER:
                    self.grid[i][j] = OBSTACLE_MARKER

    def mark_ending_point(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        #hsv for red
        hsv_low = np.array([160, 100, 100])
        hsv_high = np.array([180, 255, 255])

        mask = cv2.inRange(hsv, hsv_low, hsv_high)
        x_center_of_contour, y_center_of_contour = self.__find_center_of_contour(mask)
        self.grid[y_center_of_contour][x_center_of_contour] = ENDING_MARKER

    def mark_starting_point(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        #hsv for yellow
        hsv_low = np.array([20, 100, 100])
        hsv_high = np.array([30, 255, 255])

        mask = cv2.inRange(hsv, hsv_low, hsv_high)
        x_center_of_contour, y_center_of_contour = self.__find_center_of_contour(mask)
        self.grid[y_center_of_contour][x_center_of_contour] = STARTING_MARKER

    def __find_center_of_contour(self, mask):
        blurred = cv2.GaussianBlur(mask, (5, 5), 0)
        ret, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            M = cv2.moments(contour)
            x_center_of_contour = int(M["m10"] / M["m00"])
            y_center_of_contour = int(M["m01"] / M["m00"])
            return x_center_of_contour, y_center_of_contour


