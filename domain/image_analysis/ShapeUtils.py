import cv2
import numpy as np
import imutils

from context.config import SHAPE_UTILS_DEBUG

DEBUG = SHAPE_UTILS_DEBUG


def find_where_the_shape_is(frame, shape, color, radius_limit, scan_hsv=False):

    mask = None
    if (scan_hsv):
        hsv_frame = frame.copy()
        hsv_frame = cv2.cvtColor(hsv_frame, cv2.COLOR_BGR2HSV)
        (lower, upper) = color.color_code_hsv
        mask = cv2.inRange(hsv_frame, lower, upper)
    else:
        (lower, upper) = color.color_code

        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(frame, lower, upper)

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

    return (cX, cY)

    res_contour = get_contour_related_to_center(shape.approx, cX, cY)

    if (res_contour == 0):
        raise Exception('Can\'t find contour of the shape')

    res_contour['mask'] = mask
    return res_contour


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
    if (validate_if_contour_is_too_small(c, radius_limit, frame)):
        return (0, 0)

    M = cv2.moments(c)
    if (M["m00"] == 0.0):
        return (0, 0)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cX, cY)


def validate_if_contour_is_too_small(c, radius_limit, frame):
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    if (DEBUG):
        frame1 = frame.copy()
        cv2.circle(frame1, (round(x), round(y)), round(radius), [255, 51, 51])
        cv2.imshow('CNTS1', frame1)
        cv2.waitKey()
    if (radius < radius_limit):
        return True
    else:
        return False


def find_center_for_zone_dep(frame, c, radius_limit):
    if (validate_if_contour_is_too_small(c, radius_limit, frame)):
        return (0, 0)

    ((x, y), radius) = cv2.minEnclosingCircle(c)

    return (int(x), int(y))
