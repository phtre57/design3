import cv2 as cv2
import numpy as np


CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
NUMBER_OF_COLUMNS = 7
NUMBER_OF_LINES = 7
CHESS_SQUARE_WIDTH = 30

class PixelToXYCoordinatesConverter():

    def __init__(self, image):
        self.image = image
        self.object_points = np.zeros((NUMBER_OF_COLUMNS * NUMBER_OF_LINES, 3), np.int32)
        self.real_object_points = []
        self.image_points = []
        self.__create_real_object_points_and_image_points()

        self.x_pixel_square_width = None
        self.y_pixel_square_width = None
        self.x_pixel_to_mm_factor = None
        self.y_pixel_to_mm_factor = None

        self.__init_xy_factors()

    def __create_real_world_object_points(self):
        self.object_points[:, :2] = np.mgrid[0:NUMBER_OF_LINES, 0:NUMBER_OF_COLUMNS].T.reshape(-1, 2)

    def __create_real_object_points_and_image_points(self):
        img = cv2.imread(self.image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (NUMBER_OF_LINES, NUMBER_OF_COLUMNS), None)

        if ret:
            self.__create_real_world_object_points()
            self.real_object_points.append(self.object_points)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), CRITERIA)
            self.image_points.append(corners2)


    def __init_xy_factors(self):
        x_temp = 0
        y_temp = 0
        points = self.image_points[0]

        for i in range(1,NUMBER_OF_LINES * NUMBER_OF_COLUMNS):
            if points[i][0][0] > points[i - 1][0][0]:
                x_temp = x_temp + (points[i][0][0] - points[i - 1][0][0])

        for i in range((NUMBER_OF_LINES - 1) * NUMBER_OF_COLUMNS):
            y_temp = y_temp + points[i + NUMBER_OF_COLUMNS][0][1] - points[i][0][1]

        self.x_pixel_square_width = x_temp / (NUMBER_OF_COLUMNS * (NUMBER_OF_LINES - 1))
        self.x_pixel_to_mm_factor = CHESS_SQUARE_WIDTH / self.x_pixel_square_width

        self.y_pixel_square_width = y_temp / ((NUMBER_OF_COLUMNS - 1) * NUMBER_OF_LINES)
        self.y_pixel_to_mm_factor = CHESS_SQUARE_WIDTH / self.y_pixel_square_width

    # arg: array of pixels (i, j)
    def convert_to_xy(self, array_of_points_in_pixel):
        path = []
        for cell in array_of_points_in_pixel:
            path.append((cell.j * self.x_pixel_to_mm_factor, cell.i * self.y_pixel_to_mm_factor))

        return path



