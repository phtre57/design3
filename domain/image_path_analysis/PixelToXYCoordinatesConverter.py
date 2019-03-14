import cv2 as cv2
import numpy as np
from domain.image_path_analysis.ImageToGridConverter import *

CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
NUMBER_OF_COLUMNS = 7
NUMBER_OF_LINES = 7
CHESS_SQUARE_WIDTH = 64 #real constant used with chessboard
IMAGE_SCALE_FACTOR = 2


class PixelToXYCoordinatesConverter:

    def __init__(self, image, square_width, number_of_lines, number_of_columns):
        self.nb_lines = number_of_lines
        self.nb_columns = number_of_columns
        self.image = image.copy()
        self.square_width = square_width
        self.object_points = np.zeros((self.nb_columns * self.nb_lines, 3), np.int32)
        self.real_object_points = []
        self.image_points = []
        self.__create_real_object_points_and_image_points()

        self.x_pixel_square_width = None
        self.y_pixel_square_width = None
        self.x_pixel_to_mm_factor = None
        self.y_pixel_to_mm_factor = None

        self.__init_xy_factors()

    def __create_real_world_object_points(self):
        self.object_points[:, :2] = np.mgrid[0:self.nb_lines, 0:self.nb_columns].T.reshape(-1, 2)

    def __create_real_object_points_and_image_points(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (self.nb_lines, self.nb_columns), None)
        print("Ret value: " + str(ret))

        if ret:
            self.__create_real_world_object_points()
            self.real_object_points.append(self.object_points)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), CRITERIA)
            self.image_points.append(corners2)

            img = cv2.drawChessboardCorners(self.image, (self.nb_lines, self.nb_columns), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(0)
        else:
            print("Could not find chessboard")

    def __init_xy_factors(self):
        x_temp = 0
        y_temp = 0
        points = self.image_points[0]

        for i in range(1,self.nb_lines * self.nb_columns):
            if points[i][0][0] > points[i - 1][0][0]:
                x_temp = x_temp + (points[i][0][0] - points[i - 1][0][0])

        for i in range((self.nb_lines - 1) * self.nb_columns):
            y_temp = y_temp + points[i + self.nb_columns][0][1] - points[i][0][1]

        self.x_pixel_square_width = x_temp / (self.nb_columns * (self.nb_lines - 1))
        self.x_pixel_to_mm_factor = self.square_width / self.x_pixel_square_width

        self.y_pixel_square_width = y_temp / ((self.nb_columns - 1) * self.nb_lines)
        self.y_pixel_to_mm_factor = self.square_width / self.y_pixel_square_width

    # arg: array of pixels (i, j)
    def convert_to_xy(self, array_of_points_in_pixel):
        path = []

        #inversing y coord to be in robot referential
        for point in array_of_points_in_pixel:
            path.append((point[0] * self.x_pixel_to_mm_factor * IMAGE_SCALE_FACTOR,
                         point[1] * self.y_pixel_to_mm_factor * IMAGE_SCALE_FACTOR * -1))

        return path



