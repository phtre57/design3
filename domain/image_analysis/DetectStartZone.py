import cv2
import numpy as np

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.Canny import canny, erode_mask

"""
from ShapeValidator import ShapeValidator
from ShapeDetector import ShapeDetector
from Canny import canny, dilate_mask, erode_mask
"""

def detect_start_zone(frame):
    edges = canny(frame, erode_mask)
    shapeDetector = ShapeDetector(True, True, False)
    shapeDetector.set_peri_limiter(1000, 100000)
    shapeDetector.set_rect_limiter(90, 90)
    shapeDetector.set_radius_limiter(250, True)
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

    shapeDetector = ShapeDetector(True, True, True)
    shapeDetector.set_peri_limiter(0, 1500)
    shapeDetector.set_rect_limiter(90, 90)
    shapeDetector.set_radius_limiter(250, True)
    shape = shapeDetector.detect(output, True)

    output = cv2.bitwise_and(frame, frame, mask=output)

    return shape

# frame = cv2.imread("../../image_samples/real_image/globalmonde.jpg")
# output = detect_start_zone(frame)

# cv2.imshow('EDGES', output)
# cv2.waitKey()