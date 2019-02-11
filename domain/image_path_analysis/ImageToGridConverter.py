import numpy as np
import sys
import cv2
np.set_printoptions(threshold=sys.maxsize)

LENGTH = 320
WIDTH = 200

OBSTACLE_MARKER = 1
EMPTY_MARKER = 0
STARTING_MARKER = 2
ENDING_MARKER = 3
HSV_IN_RANGE_MARKER = 255


class ImageToGridConverter(object):
    def __init__(self, image, end_x, end_y):
        self.image = image
        self.image = cv2.resize(self.image, (LENGTH, WIDTH))
        self.grid = np.zeros((WIDTH, LENGTH))
        self.mark_starting_point()
        self.mark_ending_point(end_x, end_y)
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

    def mark_ending_point(self, end_x, end_y):
        self.grid[end_y][end_x] = ENDING_MARKER

    def mark_starting_point(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        #hsv for yellow
        hsv_low = np.array([20, 100, 100])
        hsv_high = np.array([30, 255, 255])

        mask = cv2.inRange(hsv, hsv_low, hsv_high)
        yellow_x_center_of_contour, yellow_y_center_of_contour = self.__find_center_of_contour(mask)

        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        # hsv for red
        hsv_low = np.array([160, 100, 100])
        hsv_high = np.array([180, 255, 255])

        mask = cv2.inRange(hsv, hsv_low, hsv_high)
        red_x_center_of_contour, red_y_center_of_contour = self.__find_center_of_contour(mask)

        half_distance_between_x = round(abs(yellow_x_center_of_contour - red_x_center_of_contour)/2)
        half_distance_between_y = round(abs(yellow_y_center_of_contour - red_y_center_of_contour)/2)

        if red_x_center_of_contour < yellow_x_center_of_contour:
            x_starting_pt = red_x_center_of_contour + half_distance_between_x
        else:
            x_starting_pt = yellow_x_center_of_contour + half_distance_between_x

        if red_y_center_of_contour < yellow_y_center_of_contour:
            y_starting_pt = red_y_center_of_contour + half_distance_between_y
        else:
            y_starting_pt = yellow_y_center_of_contour + half_distance_between_y

        self.grid[y_starting_pt][x_starting_pt] = STARTING_MARKER

    def __find_center_of_contour(self, mask):
        blurred = cv2.GaussianBlur(mask, (5, 5), 0)
        ret, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            M = cv2.moments(contour)
            x_center_of_contour = int(M["m10"] / M["m00"])
            y_center_of_contour = int(M["m01"] / M["m00"])
            return x_center_of_contour, y_center_of_contour


