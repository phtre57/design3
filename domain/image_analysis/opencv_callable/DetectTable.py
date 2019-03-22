import cv2
import numpy as np

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, erode_mask

PERI_LIMITER_CHECK = True
PERI_LIMITER_UPPER = 100000
PERI_LIMITER_LOWER = 1000
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 90
RECT_H_LIMITER = 90
RADIUS_LIMITER_CHECK = False


def detect_table(frame):
    frame = frame.copy()

    edges = canny(frame, erode_mask)
    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK,
                                  RADIUS_LIMITER_CHECK)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_rect_limiter(RECT_W_LIMITER, RECT_H_LIMITER)

    shape = shapeDetector.detect(edges)
    shape = shapeDetector.detect(shape.frameCnts)

    kernelerode = np.ones((2, 2), np.uint8)
    kernel = np.ones((9, 9), np.uint8)

    mask = cv2.erode(shape.frameWithText, kernelerode, iterations=1)

    output = cv2.bitwise_and(frame, frame, mask=mask)

    shape.set_frame(output)

    return shape