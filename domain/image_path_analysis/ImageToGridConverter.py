import numpy as np
import sys
import cv2
from domain.image_analysis.DetectTable import detect_table
np.set_printoptions(threshold=sys.maxsize)

LENGTH = 320
HEIGHT = 200

OBSTACLE_MARKER = 1
EMPTY_MARKER = 0
STARTING_MARKER = 2
ENDING_MARKER = 3
HSV_IN_RANGE_MARKER = 255

OBSTACLE_BORDER = 35
HORIZONTAL_WALL_BORDER = 150
VERTICAL_WALL_BORDER = 50

YELLOW_HSV_LOW = np.array([20, 100, 160])
YELLOW_HSV_HIGH = np.array([30, 255, 255])
RED_HSV_LOW = np.array([150, 100, 100])
RED_HSV_HIGH = hsv_high = np.array([180, 255, 255])
BLUE_HSV_LOW = np.array([100, 100, 120])
BLUE_HSV_HIGH = hsv_high = np.array([140, 255, 255])
BLUR_TUPLE = (5, 5)


class ImageToGridConverter(object):
    def __init__(self, image, end_x, end_y):
        self.image = image
        self.image = cv2.resize(self.image, (LENGTH, HEIGHT))
        self.grid = np.zeros((HEIGHT, LENGTH))
        self.__mark_obstacle_border()
        self.__mark_border_of_table()
        self.__mark_starting_point()
        self.__mark_ending_point(end_x, end_y)
        self.__mark_obstacle_in_grid_from_image()

    def __mark_obstacle_in_grid_from_image(self):
        self.__mark_obstacle_border()

        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, BLUE_HSV_LOW, BLUE_HSV_HIGH)
        for i in range(HEIGHT):
            for j in range(LENGTH):
                if mask[i][j] == HSV_IN_RANGE_MARKER:
                    self.grid[i][j] = OBSTACLE_MARKER

    def __mark_ending_point(self, end_x, end_y):
        self.grid[end_y][end_x] = ENDING_MARKER

    def __mark_starting_point(self):
        image = cv2.GaussianBlur(self.image, BLUR_TUPLE, 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, YELLOW_HSV_LOW, YELLOW_HSV_HIGH)
        yellow_x_center_of_contour, yellow_y_center_of_contour = self.__find_center_of_contour(mask)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, RED_HSV_LOW, RED_HSV_HIGH)
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
        ret, thresh = cv2.threshold(mask, 60, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)

            if radius > 1:
                M = cv2.moments(contour)
                x_center_of_contour = int(M["m10"] / M["m00"])
                y_center_of_contour = int(M["m01"] / M["m00"])
                return x_center_of_contour, y_center_of_contour

        raise Exception("Could not find yellow marker")

    def __find_center_of_obstacle(self, mask):
        ret, thresh = cv2.threshold(mask, 60, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        coord_array = []

        for contour in contours:
            try:
                M = cv2.moments(contour)
                x_center_of_contour = int(M["m10"] / M["m00"])
                y_center_of_contour = int(M["m01"] / M["m00"])
                coord_array.append((x_center_of_contour, y_center_of_contour))
            except Exception:
                continue

        return coord_array

    def __mark_obstacle_border(self):
        image = cv2.GaussianBlur(self.image, BLUR_TUPLE, 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, BLUE_HSV_LOW, BLUE_HSV_HIGH)
        obstacles_center_array = self.__find_center_of_obstacle(mask)

        for point in obstacles_center_array:
            x, y = point

            # loop for upper border and left border
            for i in range(OBSTACLE_BORDER * 2):
                start_y = y - OBSTACLE_BORDER
                start_x = x - OBSTACLE_BORDER

                cv2.circle(self.image, (start_x + i, start_y), 1, [255, 51, 51])
                cv2.circle(self.image, (start_x, start_y + i), 1, [255, 51, 51])

            # loop for bottom border
            for i in range(OBSTACLE_BORDER * 2):
                start_y = y + OBSTACLE_BORDER
                start_x = x - OBSTACLE_BORDER

                cv2.circle(self.image, (start_x + i, start_y), 1, [255, 51, 51])

            # loop for right border
            for i in range(OBSTACLE_BORDER * 2):
                start_y = y - OBSTACLE_BORDER
                start_x = x + OBSTACLE_BORDER

                cv2.circle(self.image, (start_x, start_y + i), 1, [255, 51, 51])

    def __mark_border_of_table(self):
        image = self.image.copy()
        shape = detect_table(image)
        x_center_of_contour = 0
        y_center_of_contour = 0

        for contour in shape.cnts:
            try:
                M = cv2.moments(contour)
                x_center_of_contour = int(M["m10"] / M["m00"])
                y_center_of_contour = int(M["m01"] / M["m00"])
            except Exception:
                continue

        #bottom border
        for i in range(HORIZONTAL_WALL_BORDER * 2):
            start_y = y_center_of_contour + VERTICAL_WALL_BORDER
            start_x = x_center_of_contour - HORIZONTAL_WALL_BORDER

            cv2.circle(self.image, (start_x + i, start_y), 1, [255, 51, 51])

        #Upper border
        for i in range(HORIZONTAL_WALL_BORDER * 2):
            start_y = y_center_of_contour - VERTICAL_WALL_BORDER
            start_x = x_center_of_contour - HORIZONTAL_WALL_BORDER

            cv2.circle(self.image, (start_x + i, start_y), 1, [255, 51, 51])

        #rigth border
        for i in range(VERTICAL_WALL_BORDER * 2):
            start_y = y_center_of_contour - VERTICAL_WALL_BORDER
            start_x = x_center_of_contour + HORIZONTAL_WALL_BORDER

            cv2.circle(self.image, (start_x, start_y + i), 1, [255, 51, 51])

        #left border
        for i in range(VERTICAL_WALL_BORDER * 2):
            start_y = y_center_of_contour - VERTICAL_WALL_BORDER
            start_x = x_center_of_contour - HORIZONTAL_WALL_BORDER

            cv2.circle(self.image, (start_x, start_y + i), 1, [255, 51, 51])