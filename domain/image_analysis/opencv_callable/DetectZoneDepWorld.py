import cv2
import numpy as np

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import *
from domain.image_analysis.ShapeUtils import *

PERI_LIMITER_CHECK = True
PERI_LIMITER_UPPER = 100000
PERI_LIMITER_LOWER = 1000
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 90
RECT_H_LIMITER = 90
RADIUS_LIMITER_CHECK = False


def detect_zone_dep_world(frame):
    frame = frame.copy()

    edges = canny(frame, erode_mask)
    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK,
                                  RADIUS_LIMITER_CHECK)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_rect_limiter(RECT_W_LIMITER, RECT_H_LIMITER)
    shapeDetector.set_shape_only("rectangle")

    shape = shapeDetector.detect(edges)
    shape = shapeDetector.detect(shape.frameCnts)

    # kernelerode = np.ones((2, 2), np.uint8)
    kernel = np.ones((9, 9), np.uint8)

    mask = shape.frameWithText
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20)))
    # mask = cv2.erode(shape.frameWithText, kernelerode, iterations = 1)

    output = cv2.bitwise_and(frame, frame, mask=mask)
    output = canny(output, erode_mask_zone_dep)

    output = cv2.morphologyEx(
        output, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20)))
    output = cv2.morphologyEx(output, cv2.MORPH_OPEN, kernel)

    shapeDetector = ShapeDetector(True, True, True)
    shapeDetector.set_peri_limiter(180, 200)
    shapeDetector.set_rect_limiter(20, 20)
    shapeDetector.set_radius_limiter(50, True)
    shape = shapeDetector.detect(output)

    output = cv2.bitwise_and(frame, frame, mask=shape.frameCnts)

    shape.set_frame(output)

    if (len(shape.approx) > 1):
        print("Ça pas marché")
        shape.center = (0, 0)
        return shape

    shape.center = find_center(shape.approx[0][2], 10)
    shape.center = adjust_start_zone_offset(shape.center)

    return shape


def adjust_start_zone_offset(point):
    # Faire les deux bords de la table avec un beau if
    if (point[1] > 120):
        return (point[0], point[1] - 35)
    else:
        return (point[0], point[1] + 35)
