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


class ImageToGridConverter(object):
    def __init__(self, image):
        self.image = image
        self.image = cv2.resize(self.image, (LENGTH, WIDTH))
        self.grid = np.zeros((WIDTH, LENGTH))

    def convert_image_to_grid(self):
        return 0

    def mark_obstacle_in_grid_from_image(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        hsv_low = np.array([100, 150, 0])
        hsv_high = np.array([140, 255, 255])

        mask = cv2.inRange(hsv, hsv_low, hsv_high)
        for i in range(WIDTH):
            for j in range(LENGTH):
                if mask[i][j] == 1:
                    self.grid[i][j] = OBSTACLE_MARKER
                    print("found")

    def __show_image(self, image):
        cv2.imshow("real", image)


img = cv2.imread("../../image_samples/test_table.png")
test_image = ImageToGridConverter(img)
test_image.mark_obstacle_in_grid_from_image()

