import numpy as np
import sys
import cv2
import imutils
np.set_printoptions(threshold=sys.maxsize)

LENGTH = 320
HEIGHT = 240

OBSTACLE_MARKER = 1
EMPTY_MARKER = 0
STARTING_MARKER = 2
ENDING_MARKER = 3
HSV_IN_RANGE_MARKER = 255

OBSTACLE_BORDER = 35

X_WALL_LEFT_CORNER = 20
X_WALL_RIGHT_CORNER = 300
Y_WALL_UP_CORNER = 60
Y_WALL_DOWN_CORNER = 180


BLUE_HSV_LOW = np.array([100, 100, 120])
BLUE_HSV_HIGH = hsv_high = np.array([140, 255, 255])
BLUR_TUPLE = (3, 3)


class ImageToGridConverter(object):
    def __init__(self, image, x_start, y_start, x_end, y_end):
        self.image = image.copy()
        self.image = cv2.resize(self.image, (LENGTH, HEIGHT))
        self.image = cv2.GaussianBlur(self.image, BLUR_TUPLE, 0)
        self.grid = np.zeros((HEIGHT, LENGTH))
        self.mark_starting_point(x_start, y_start)
        self.mark_ending_point(x_end, y_end)
        self.__mark_obstacle_border()
        self.__mark_table_wall()
        self.mark_obstacle_in_grid_from_image()

    def mark_obstacle_in_grid_from_image(self):

        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, BLUE_HSV_LOW, BLUE_HSV_HIGH)
        for i in range(HEIGHT):
            for j in range(LENGTH):
                if mask[i][j] == HSV_IN_RANGE_MARKER:
                    self.grid[i][j] = OBSTACLE_MARKER

    def mark_ending_point(self, x_end, y_end):
        self.grid[y_end][x_end] = ENDING_MARKER

    def mark_starting_point(self, x_start, y_start):
        self.grid[y_start][x_start] = STARTING_MARKER

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
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

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

    def __mark_table_wall(self):
        for i in range(X_WALL_RIGHT_CORNER - X_WALL_LEFT_CORNER):
            start_x = X_WALL_LEFT_CORNER + i

            cv2.circle(self.image, (start_x, Y_WALL_UP_CORNER), 1, [255, 51, 51])

        for i in range(X_WALL_RIGHT_CORNER - X_WALL_LEFT_CORNER):
            start_x = X_WALL_LEFT_CORNER + i

            cv2.circle(self.image, (start_x, Y_WALL_DOWN_CORNER), 1, [255, 51, 51])

        for i in range(Y_WALL_DOWN_CORNER - Y_WALL_UP_CORNER):
            cv2.circle(self.image, (X_WALL_LEFT_CORNER, Y_WALL_UP_CORNER + i), 1, [255, 51, 51])

        for i in range(Y_WALL_DOWN_CORNER - Y_WALL_UP_CORNER):
            cv2.circle(self.image, (X_WALL_RIGHT_CORNER, Y_WALL_UP_CORNER + i), 1, [255, 51, 51])

