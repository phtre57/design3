import cv2
import numpy as np
import imutils

from ShapeValidator import ShapeValidator
from ShapeDetector import ShapeDetector
from Canny import canny, dilate_mask, erode_mask

def color_detector(frame):
    edges = canny(frame, dilate_mask)
    shapeDetector = ShapeDetector(True, True, True)
    shapeDetector.set_peri_limiter(150, 700)
    shapeDetector.set_rect_limiter(10, 10)
    shapeDetector.set_radius_limiter(90, True)
    shape = shapeDetector.detect(edges, False)

    kernel = np.ones((9, 9), np.uint8)
    kernelerode = np.ones((9,9),np.uint8)

    shape = shapeDetector.detect(edges, True)

    output = cv2.bitwise_and(frame, frame, mask=edges)

    mask = output
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10)))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10)))
    mask = cv2.erode(mask,kernelerode,iterations = 1)

    output = mask
    # print(shape)
    return output


frame = cv2.imread("../../image_samples/real_image/pieces.jpg")
output = color_detector(frame)
cv2.imshow('EDGES', output)

cv2.waitKey()

