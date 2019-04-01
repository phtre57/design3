import cv2
from domain.image_analysis.ImageToGridConverter import *

SAFETY = 10


def find_center_of_obstacle(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, BLUE_HSV_LOW, BLUE_HSV_HIGH)
    ret, thresh = cv2.threshold(mask, 60, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
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


def get_x_range(img, y):
    img = cv2.resize(img, (LENGTH, HEIGHT))
    centers_of_obstacle = find_center_of_obstacle(img)

    x_range = []

    for points in centers_of_obstacle:
        if points[1] <= y + OBSTACLE_BORDER or points[1] >= y - OBSTACLE_BORDER:
            x_range.append((points[0] + OBSTACLE_BORDER + SAFETY,
                            LENGTH - (LENGTH - X_WALL_RIGHT_CORNER) - SAFETY))
            break

    if len(x_range) == 0:
        x_range.append((LENGTH / 2, LENGTH - X_WALL_RIGHT_CORNER - SAFETY))

    return x_range