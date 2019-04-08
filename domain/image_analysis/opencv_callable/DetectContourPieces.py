import cv2

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, detect_contour_mask
from domain.image_analysis.ShapeUtils import find_center
from domain.QRCodeDictionnary import *
from domain.image_analysis.opencv_callable.ref_shape import *
from util.Logger import Logger

PERI_LIMITER_CHECK = False
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 180
RECT_H_LIMITER = 180
RECT_W_LIMITER_UP = 260
RECT_H_LIMITER_UP = 260
RADIUS_LIMITER_CHECK = False
RAIDUS_POSITIVE = True

logger = Logger(__name__)

DEBUG = False


def detect_contour_pieces(og_frame, _str_shape):
    str_shape = translate_str_shape(_str_shape)

    logger.log_info('DETECT CONTOUR PIECES received ' + str(_str_shape) +
                    ' translated it to ' + str(str_shape))

    frame = og_frame.copy()
    frame = frame.copy()

    w, h, c = frame.shape

    factorw = round(w / 240)
    factorh = round(h / 320)

    cv2.rectangle(frame, (240 * factorh, 0 * factorw),
                  (320 * factorh, 240 * factorw), (0, 0, 0), 110 * factorh)
    cv2.rectangle(frame, (0 * factorh, 200 * factorw),
                  (320 * factorh, 240 * factorw), (0, 0, 0), 110 * factorh)

    edges = canny(frame, detect_contour_mask, 150, 200)

    edges = cv2.dilate(
        edges,
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)),
        iterations=1)

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
    shape.set_frame(shape.frameClean)

    if DEBUG:
        cv2.imshow('ok', shape.frame)
        cv2.waitKey()

    if (len(shape.approx) != 1):
        raise Exception('Detect contour pieces have found multiple shape')

    (x, y) = find_center(shape.approx[0][1], 50, shape.frame)

    print(x, y)

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
