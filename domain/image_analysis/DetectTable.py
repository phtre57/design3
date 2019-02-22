import cv2
import numpy as np

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.Canny import canny, erode_mask

"""
from ShapeValidator import ShapeValidator
from ShapeDetector import ShapeDetector
from Canny import canny, dilate_mask, erode_mask
"""

def detect_table(frame):
    frame = frame.copy()
    
    edges = canny(frame, erode_mask)
    shapeDetector = ShapeDetector(True, True, True)
    shapeDetector.set_peri_limiter(1000, 100000)
    shapeDetector.set_rect_limiter(90, 90)
    shapeDetector.set_radius_limiter(100, False)

    shape = shapeDetector.detect(edges)
    shape = shapeDetector.detect(shape.frameCnts)

    kernelerode = np.ones((2,2),np.uint8)
    kernel = np.ones((9, 9), np.uint8)

    mask = cv2.erode(shape.frameWithText,kernelerode,iterations = 1)

    output = cv2.bitwise_and(frame, frame, mask=mask)

    shape.set_frame(output)

    return shape