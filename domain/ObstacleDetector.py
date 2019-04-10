import cv2
import numpy as np

BLUE_HSV_LOW = np.array([100, 100, 120])
BLUE_HSV_HIGH = hsv_high = np.array([140, 255, 255])


class ObstacleDetector:

    def __init__(self, img):
        self.image = img.copy()

    def find_center_of_obstacle(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, BLUE_HSV_LOW, BLUE_HSV_HIGH)

        ret, thresh = cv2.threshold(mask, 60, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
        coord_array = []

        for contour in contours:
            try:
                perimeter = cv2.arcLength(contour, True)

                if perimeter < 1:
                    continue

                M = cv2.moments(contour)
                x_center_of_contour = int(M["m10"] / M["m00"])
                y_center_of_contour = int(M["m01"] / M["m00"])
                coord_array.append((x_center_of_contour, y_center_of_contour))
            except Exception:
                continue

        return coord_array