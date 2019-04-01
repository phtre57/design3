import cv2
import numpy as np

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, erode_mask
from domain.image_analysis.ShapeUtils import *
from context.config import *
from util.Logger import Logger

PERI_LIMITER_CHECK = False
PERI_LIMITER_UPPER = 3000
PERI_LIMITER_LOWER = 700
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 155
RECT_H_LIMITER = 155
RECT_W_LIMITER_UP = 240
RECT_H_LIMITER_UP = 240

HC_RECT_W_LIMITER = 165
HC_RECT_H_LIMITER = 165
HC_RECT_W_LIMITER_UP = None
HC_RECT_H_LIMITER_UP = None

RADIUS_LIMITER_CHECK = False
RADIUS_LIMITER = 250
RAIDUS_POSITIVE = True

DEBUG = DETECT_START_ZONE_DEBUG

logger = Logger(__name__)


def detect_start_zone(og_frame, alpha=1.5):
    frame = og_frame.copy()
    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=100)
    
    edges = canny(frame, erode_mask)

    if (DEBUG):
        cv2.imshow('DEBUG', edges)
        cv2.waitKey()

    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK,
                                  RADIUS_LIMITER_CHECK)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_rect_limiter(RECT_W_LIMITER, RECT_H_LIMITER, None,
                                   RECT_W_LIMITER_UP, RECT_H_LIMITER_UP)
    shape = shapeDetector.detect(edges, og_frame.copy())

    mask = shape.frameClean

    if (DEBUG):
        cv2.imshow('FRAME CLEAN', mask)
        cv2.waitKey()

    output = cv2.bitwise_and(frame, frame, mask=mask)
    shape.set_frame(output)

    __decision(shape)

    (x, y) = find_center_for_zone_dep(frame, shape.approx[0][2], 100)

    logger.log_debug('START ZONE - Found center ' + str(x) + ' ' + str(y))
    cv2.circle(shape.frame, (x, y), 1, [255, 51, 51])

    return (x, y)

def __decision(shape):
    if (len(shape.approx) == 0):
        cv2.imshow('RAISE', shape.frame)
        cv2.waitKey()
        raise Exception("Can't find start zone", len(shape.approx))
    else:
        shape.approx = shape.approx[:1]
        logger.log_warning(
            'Found multiples possible start zone, took the first one')