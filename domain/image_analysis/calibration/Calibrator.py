import cv2
import numpy as np

CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
NUMBER_OF_COLUMNS = 7
NUMBER_OF_LINES = 7
CHESS_SQUARE_WIDTH = 43 #real constant used with chessboard


class Calibrator:

    def __init__(self, image, number_of_lines, number_of_columns):
        self.image = image.copy()
        self.nb_lines = number_of_lines
        self.nb_columns = number_of_columns
        self.object_points = np.zeros((self.nb_columns * self.nb_lines, 3), np.float32)
        self.real_object_points = []
        self.image_points = []
        self.mtx = None

        self.__create_real_object_points_and_image_points()

    def __create_real_world_object_points(self):
        self.object_points[:, :2] = np.mgrid[0:self.nb_lines, 0:self.nb_columns].T.reshape(-1, 2)

    def __create_real_object_points_and_image_points(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (self.nb_lines, self.nb_columns), None)

        if ret:
            self.__create_real_world_object_points()
            self.real_object_points.append(self.object_points)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), CRITERIA)
            self.image_points.append(corners2)

            img = cv2.drawChessboardCorners(self.image, (self.nb_lines, self.nb_columns), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(0)

    def calibrate_camera(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.real_object_points, self.image_points, gray.shape[::-1], None, None)

        h, w = self.image.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

        # undistort
        dst = cv2.undistort(self.image, mtx, dist, None, newcameramtx)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]

        cv2.imshow("undistorted", dst)
        cv2.waitKey(0)


img = cv2.imread("calibration2.jpg")

calibrator = Calibrator(img, NUMBER_OF_LINES,  NUMBER_OF_COLUMNS)
calibrator.calibrate_camera()






