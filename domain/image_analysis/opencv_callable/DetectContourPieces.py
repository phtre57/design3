import cv2

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, detect_contour_mask
from domain.image_analysis.ShapeUtils import find_center
from domain.QRCodeDictionnary import *
from util.Logger import Logger

PERI_LIMITER_CHECK = False
PERI_LIMITER_UPPER = 160
PERI_LIMITER_LOWER = 100
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 40
RECT_H_LIMITER = 40
RECT_W_LIMITER_UP = 60
RECT_H_LIMITER_UP = 60
RADIUS_LIMITER_CHECK = False
RADIUS_LIMITER = 90
RAIDUS_POSITIVE = True

logger = Logger(__name__)

DEBUG = True


def detect_contour_pieces(og_frame, _str_shape):
    str_shape = translate_str_shape(_str_shape)

    logger.log_info('DETECT CONTOUR PIECES received ' + str(_str_shape) +
                    ' translated it to ' + str(str_shape))

    frame = og_frame.copy()
    frame = frame.copy()

    cv2.rectangle(frame, (200, 0), (320, 240), (0, 0, 0), 110)
    cv2.rectangle(frame, (245, 0), (320, 240), (0, 0, 0), 110)

    edges = canny(frame, detect_contour_mask, 170, 200)

    if DEBUG:
        cv2.imshow('ok', edges)
        cv2.waitKey()

    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK,
                                  RADIUS_LIMITER_CHECK)
    shapeDetector.set_rect_limiter(
        RECT_W_LIMITER,
        RECT_H_LIMITER,
        None,
        h_rect_limit_up=RECT_H_LIMITER_UP,
        w_rect_limit_up=RECT_W_LIMITER_UP)
    shapeDetector.set_shape_only(str_shape)
    shapeDetector.set_external_cnts(True)

    shape = shapeDetector.detect(edges, og_frame.copy())
    shape.set_frame(shape.frameWithText)

    if (len(shape.approx) != 1):
        raise Exception('Detect contour pieces have found multiple shape')

    (x, y) = find_center(shape.approx[0][1], 4, shape)

    return (x, y)


def translate_str_shape(str_shape):
    if (str_shape == CARRE):
        return 'squaretangle'
    elif (str_shape == CERCLE):
        return 'circle'
    elif (str_shape == TRIANGLE):
        return 'triangle'
    elif (str_shape == PENTAGON):
        return 'pentagon'
