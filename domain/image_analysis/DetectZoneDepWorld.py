import cv2
import numpy as np
import imutils

from ShapeValidator import ShapeValidator
from ShapeDetector import ShapeDetector
from Canny import canny, dilate_mask, erode_mask

def detect_zone_dep_world(frame):
    edges = canny(frame, erode_mask)
    shapeDetector = ShapeDetector(True, True, False)
    shapeDetector.set_peri_limiter(1000, 100000)
    shapeDetector.set_rect_limiter(90, 90)
    shape = shapeDetector.detect(edges, False)
    shape = shapeDetector.detect(edges, True)

    kernelerode = np.ones((2,2),np.uint8)
    kernel = np.ones((9, 9), np.uint8)

    edges = cv2.erode(edges,kernelerode,iterations = 1)

    output = cv2.bitwise_and(frame, frame, mask=edges)

    output = canny(output, erode_mask)

    mask = output
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20)))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    output = mask

    shapeDetector = ShapeDetector(True, False, True)
    shapeDetector.set_peri_limiter(0, 1000)
    shapeDetector.set_radius_limiter(50, True)
    shapeDetector.set_shape_only("rectangle")
    shape = shapeDetector.detect(output, True)

    output = cv2.bitwise_and(frame, frame, mask=output)

    print(shape)

    return output

frame = cv2.imread("../../image_samples/real_image/globalmonde.jpg")
output = detect_zone_dep_world(frame)

cv2.imshow('EDGES', output)
cv2.waitKey()