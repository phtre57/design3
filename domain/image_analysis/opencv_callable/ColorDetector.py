import cv2

from util.color import Color
from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, dilate_mask
from domain.image_analysis.ShapeUtils import *
from context.config import COLOR_DETECTOR_DEBUG

RADIUS_LIMIT = 2

PERI_LIMITER_CHECK = True
PERI_LIMITER_UPPER = 160
PERI_LIMITER_LOWER = 100
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 20
RECT_H_LIMITER = 20
RADIUS_LIMITER_CHECK = True
RADIUS_LIMITER = 90
RAIDUS_POSITIVE = True

DEBUG = COLOR_DETECTOR_DEBUG


def color_detector(frame, color):
    frame = frame.copy()

    shape = create_mask_for_color_detector(frame)

    if (DEBUG):
        cv2.imshow("SHAPE", shape.frame)
        cv2.waitKey()

    shape.res_contour = find_where_the_shape_is(shape, color, RADIUS_LIMIT,
                                                True)

    return (shape.res_contour['point'][0], shape.res_contour['point'][1])


def create_mask_for_color_detector(og_frame):
    frame = og_frame.copy()

    edges = canny(frame, dilate_mask)
    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK,
                                  RADIUS_LIMITER_CHECK)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_rect_limiter(RECT_W_LIMITER, RECT_H_LIMITER)
    shapeDetector.set_radius_limiter(RADIUS_LIMITER, RAIDUS_POSITIVE)

    shape = shapeDetector.detect(edges, og_frame.copy())
    shape = shapeDetector.detect(shape.frameCnts, og_frame.copy())

    mask = cv2.bitwise_and(frame, frame, mask=shape.frameWithText)

    # kernel = np.ones((9, 9), np.uint8)
    kernelerode = np.ones((9, 9), np.uint8)

    mask = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)))
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)))
    mask = cv2.erode(mask, kernelerode, iterations=1)

    shape.set_frame(mask)

    return shape
