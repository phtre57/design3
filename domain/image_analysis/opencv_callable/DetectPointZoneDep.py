import cv2

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, point_zone_dep_mask
from domain.image_analysis.ShapeUtils import find_center
from context.config import *

PERI_LIMITER_CHECK = False
PERI_LIMITER_UPPER = 160
PERI_LIMITER_LOWER = 100
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 6
RECT_H_LIMITER = 6
RECT_W_LIMITER_UP = 14
RECT_H_LIMITER_UP = 14

RADIUS_LIMITER_CHECK = True
RADIUS_LIMITER = 7
RAIDUS_POSITIVE = True

DEBUG = DETECT_POINT_ZONE_DEP_DEBUG


def detect_point_zone_dep(og_frame):
    frame = og_frame.copy()

    cv2.rectangle(frame, (270, 0), (320, 240), (0, 0, 0), 110)
    cv2.rectangle(frame, (0, 200), (320, 240), (0, 0, 0), 110)

    edges = canny(frame, point_zone_dep_mask, 80, 100)

    edges = cv2.dilate(
        edges,
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)),
        iterations=1)

    if DEBUG:
        cv2.imshow('DETECT ZONE DEP -- DEBUG', edges)
        cv2.waitKey()

    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK,
                                  RADIUS_LIMITER_CHECK)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_rect_limiter(
        RECT_W_LIMITER,
        RECT_H_LIMITER,
        None,
        w_rect_limit_up=RECT_W_LIMITER_UP,
        h_rect_limit_up=RECT_H_LIMITER_UP)
    shapeDetector.set_radius_limiter(RADIUS_LIMITER, RAIDUS_POSITIVE)
    shapeDetector.set_coord_limiter(0)
    shape = shapeDetector.detect(edges, og_frame.copy())

    shape.set_frame(shape.frameClean)

    # if (len(shape.approx) != 1):
    #     raise Exception('Detect contour pieces have found multiple shape')

    (x, y) = find_center(shape.approx[0][1], 4, shape)

    return (x, y)
