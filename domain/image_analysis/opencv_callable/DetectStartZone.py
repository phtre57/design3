import cv2
import numpy as np

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, erode_mask
from domain.image_analysis.ShapeUtils import *

PERI_LIMITER_CHECK = True
PERI_LIMITER_UPPER = 100000
PERI_LIMITER_LOWER = 1000
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 90
RECT_H_LIMITER = 90
RADIUS_LIMITER_CHECK = False
RADIUS_LIMITER = 250
RAIDUS_POSITIVE = True


def detect_start_zone(frame):
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

    output = canny(output, erode_mask)

    output = cv2.morphologyEx(
        output, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20)))
    output = cv2.morphologyEx(output, cv2.MORPH_OPEN, kernel)

    shapeDetector = ShapeDetector(True, True, True)
    shapeDetector.set_peri_limiter(0, 1500)
    shapeDetector.set_rect_limiter(90, 90)
    shapeDetector.set_radius_limiter(250, True)
    shape = shapeDetector.detect(output)

    output = cv2.bitwise_and(frame, frame, mask=shape.frameWithText)

    shape.set_frame(output)

    cv2.imshow("ok", output)
    cv2.waitKey()
    if (len(shape.approx) > 1 or len(shape.approx) == 0):
        print("Ça pas marché")
        shape.center = (0, 0)
        return shape

    shape.center = find_center_for_zone_dep(shape, 100)

    cv2.circle(shape.frame, (shape.center[0], shape.center[1]), 1,
               [255, 51, 51])

    # shape.center = find_center(shape.approx[0][2], 100)

    return shape
