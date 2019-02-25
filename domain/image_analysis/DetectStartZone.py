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
    frame.copy()

    edges = canny(frame, erode_mask)
    shapeDetector = ShapeDetector(True, True, False)
    shapeDetector.set_peri_limiter(1000, 100000)
    shapeDetector.set_rect_limiter(90, 90)
    shapeDetector.set_radius_limiter(250, True)

    shape = shapeDetector.detect(edges)
    shape = shapeDetector.detect(shape.frameCnts)

    kernelerode = np.ones((2,2),np.uint8)
    kernel = np.ones((9, 9), np.uint8)

    mask = cv2.erode(shape.frameWithText, kernelerode, iterations = 1)

    output = cv2.bitwise_and(frame, frame, mask=mask)

    output = canny(output, erode_mask)

    output = cv2.morphologyEx(output, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20)))
    output = cv2.morphologyEx(output, cv2.MORPH_OPEN, kernel)

    shapeDetector = ShapeDetector(True, True, True)
    shapeDetector.set_peri_limiter(0, 1500)
    shapeDetector.set_rect_limiter(90, 90)
    shapeDetector.set_radius_limiter(250, True)
    shape = shapeDetector.detect(output)

    output = cv2.bitwise_and(frame, frame, mask=shape.frameWithText)

    shape.set_frame(output)

    return shape