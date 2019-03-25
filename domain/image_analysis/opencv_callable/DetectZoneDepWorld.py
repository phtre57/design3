import cv2
import numpy as np

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import *
from domain.image_analysis.ShapeUtils import *

PERI_LIMITER_CHECK = False
PERI_LIMITER_UPPER = 100000
PERI_LIMITER_LOWER = 150
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 60
RECT_H_LIMITER = 10
RADIUS_LIMITER_CHECK = False
RADIUS_LIMITER = 30
RAIDUS_POSITIVE = False

OFFSET_PATHFINDING = 40

DEBUG = True


def detect_zone_dep_world(og_frame):
    frame = og_frame.copy()
    frame = frame.copy()

    edges = canny(frame, erode_mask_zone_dep_world, 10, 150)
    edges = cv2.morphologyEx(
        edges, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    kernelerode = np.ones((3, 3), np.uint8)
    edges = cv2.erode(edges, kernelerode, iterations=1)

    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK,
                                  RADIUS_LIMITER_CHECK)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_rect_limiter(RECT_W_LIMITER, RECT_H_LIMITER)

    shape = shapeDetector.detect(edges, og_frame.copy())

    if DEBUG:
        cv2.imshow('frameClean', shape.frameClean)
        cv2.waitKey()

    output = cv2.bitwise_and(frame, frame, mask=shape.frameClean)

    shape.set_frame(output)

    if (len(shape.approx) > 1 or len(shape.approx) == 0):
        raise Exception("Can't find zone depot " + str(len(shape.approx)))

    shape.center = find_center(shape.approx[0][2], 10)
    shape.center = adjust_start_zone_offset(shape.center)

    cv2.circle(shape.frame, (shape.center[0], shape.center[1]), 1,
               [255, 51, 51])

    return shape


def adjust_start_zone_offset(point):
    # Faire les deux bords de la table avec un beau if
    if (point[1] > 120):
        return (point[0], point[1] - OFFSET_PATHFINDING)
    else:
        return (point[0], point[1] + OFFSET_PATHFINDING)
