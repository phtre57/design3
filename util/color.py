import numpy as np

# YELLOW_HSV_LOW = np.array([10, 205, 215])
# YELLOW_HSV_HIGH = np.array([80, 255, 255])

YELLOW_HSV_LOW = np.array([20, 220, 220])
YELLOW_HSV_HIGH = np.array([80, 250, 255])

# RED_HSV_LOW = np.array([0, 60, 100])
# RED_HSV_HIGH = np.array([10, 255, 255])

RED_HSV_LOW = np.array([0, 60, 100])
RED_HSV_HIGH = np.array([0, 255, 255])

# BLUE_HSV_LOW = np.array([80, 15, 120])
# BLUE_HSV_HIGH = np.array([140, 255, 255])

BLUE_HSV_LOW = np.array([100, 15, 150])
BLUE_HSV_HIGH = np.array([140, 255, 255])

# GREEN_HSV_LOW = np.array([40, 40, 60])
# GREEN_HSV_HIGH = np.array([80, 130, 255])

GREEN_HSV_LOW = np.array([55, 40, 60])
GREEN_HSV_HIGH = np.array([80, 255, 255])


class Color:
    def __init__(self):
        self.color = 0

    def RED(self):
        self.color = 1
        self.color_code = ([0, 0, 170], [255, 110, 255])
        self.color_code_hsv = (RED_HSV_LOW, RED_HSV_HIGH)
        self.color_code_hsv_str = '0, 60, 100 | 0, 255, 255'

    def GREEN(self):
        self.color = 2
        # self.color_code = ([0, 119, 0], [122, 255, 28])
        self.color_code = ([0, 120, 0], [151, 255, 127])
        self.color_code_hsv = (GREEN_HSV_LOW, GREEN_HSV_HIGH)
        self.color_code_hsv_str = '55, 40, 60 | 80, 255, 255'

    def BLUE(self):
        self.color = 3
        self.color_code = ([130, 49, 0], [255, 255, 65])
        self.color_code_hsv = (BLUE_HSV_LOW, BLUE_HSV_HIGH)
        self.color_code_hsv_str = '80, 15, 120 | 140, 255, 255'

    def YELLOW(self):
        self.color = 4
        self.color_code = ([4, 11, 234], [255, 255, 255])
        self.color_code_hsv = (YELLOW_HSV_LOW, YELLOW_HSV_HIGH)
        self.color_code_hsv_str = '20, 220, 220 | 80, 250, 255'

    def ORANGE(self):
        self.color = 5
        self.YELLOW()
