import cv2
import numpy as np
import imutils
import base64

from context.config import SHAPE_UTILS_DEBUG
from util.Logger import Logger

DEBUG = SHAPE_UTILS_DEBUG

logger = Logger(__name__)


def find_where_the_shape_is(frame, shape, color, radius_limit):
    mask = None

    hsv_frame = frame.copy()
    hsv_frame = cv2.cvtColor(hsv_frame, cv2.COLOR_BGR2HSV)
    (lower, upper) = color.color_code_hsv
    mask = cv2.inRange(hsv_frame, lower, upper)

    if (DEBUG):
        cv2.imshow("COLOR FILTER", mask)
        cv2.waitKey()

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    (cX, cY) = (0, 0)
    for c in cnts:
        (cX, cY) = find_center(c, radius_limit, mask)
        if (cX != 0 and cY != 0):
            break

    if (cX == 0 and cY == 0):
        raise Exception('Can\'t find center of the shape')

    # frame1 = frame.copy()
    # cv2.circle(frame1, (cX, cY), round(10), [255, 255, 255])
    # _, buffer = cv2.imencode('.jpg', frame1)
    # encoded = base64.b64encode(buffer)
    # logger.log_debug('IMAGE OF COLOR DETECTOR ' + str(encoded))

    return (cX, cY)


def get_contour_related_to_center(approx, cX, cY):
    is_in = False
    for contour in approx:
        is_in = cv2.pointPolygonTest(contour[1], (cX, cY), False)
        if (is_in):
            res_contour = {}
            res_contour['contour'] = contour
            res_contour['point'] = (cX, cY)
            return res_contour
    return 0


def find_center(c, radius_limit, frame):
    center_or_none = validate_if_contour_is_too_small(c, radius_limit, frame)
    if (center_or_none is True):
        return (0, 0)

    return center_or_none

    M = cv2.moments(c)
    if (M["m00"] == 0.0):
        return (0, 0)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cX, cY)


def validate_if_contour_is_too_small(c, radius_limit, frame):
    ((x, y), radius) = cv2.minEnclosingCircle(c)

    if (DEBUG):
        print(radius)
        print(radius_limit)
        frame1 = frame.copy()
        cv2.circle(frame1, (round(x), round(y)), round(radius), [255, 51, 51])
        cv2.imshow('CNTS1', frame1)
        cv2.waitKey()

    if (radius < radius_limit):
        return True
    else:
        return (round(x), round(y))


def find_center_for_zone_dep(frame, c, radius_limit):
    center_or_none = validate_if_contour_is_too_small(c, radius_limit, frame)

    if (center_or_none is True):
        return (0, 0)

    ((x, y), radius) = cv2.minEnclosingCircle(c)

    return (int(x), int(y))
