import cv2
import numpy as np

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, erode_mask
from domain.image_analysis.ShapeUtils import *

PERI_LIMITER_CHECK = True
PERI_LIMITER_UPPER = 1000
PERI_LIMITER_LOWER = 300
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 150
RECT_H_LIMITER = 150
RADIUS_LIMITER_CHECK = False
RADIUS_LIMITER = 250
RAIDUS_POSITIVE = True


def detect_pickup_zone(og_frame):
    frame = og_frame.copy()

    edges = canny(frame, erode_mask)
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)
    cv2.imshow("CANNY", edges)
    cv2.waitKey()

    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK,
                                  RADIUS_LIMITER_CHECK)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_rect_limiter(RECT_W_LIMITER, RECT_H_LIMITER)

    shape = shapeDetector.detect(edges, og_frame.copy())

    mask = shape.frameClean
    output = cv2.bitwise_and(frame, frame, mask=mask)

    shape.set_frame(output)

    if (len(shape.approx) > 1 or len(shape.approx) == 0):
        raise Exception("Can't find start zone")

    shape.center = find_center_for_zone_dep(shape, 100)

    cv2.circle(shape.frame, (shape.center[0], shape.center[1]), 1,
               [255, 51, 51])

    return shape
