import cv2
import numpy as np
import imutils

from util.color import Color
from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, dilate_mask

PERI_LIMITER_CHECK = True
PERI_LIMITER_UPPER = 700
PERI_LIMITER_LOWER = 150
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 10
RECT_H_LIMITER = 10
RADIUS_LIMITER_CHECK = True
RADIUS_LIMITER = 90
RAIDUS_POSITIVE = True

def color_detector(frame, color):
    frame = frame.copy()

    shape = create_mask_for_color_detector(frame)    

    res_contour = find_where_the_shape_is(shape, color)
    shape.res_contour = res_contour
    return shape

def find_where_the_shape_is(shape, color):
    (lower, upper) = color.color_code

    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(shape.frame, lower, upper)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    (cX, cY) = find_center(cnts)

    if (cX == 0 and cY == 0):
        print("Ça pas marché")

    res_contour = get_contour_related_to_center(shape.approx, cX, cY)

    if (res_contour == 0):
        print("Ça pas marché")

    res_contour.append(mask)
    return res_contour

def get_contour_related_to_center(approx, cX, cY):
    is_in = False
    for contour in approx:
        is_in = cv2.pointPolygonTest(contour[1], (cX, cY), False)
        if (is_in):
            res_contour = contour
            res_contour.append((cX, cY))
            return res_contour
    return 0

def find_center(cnts):
    for c in cnts:
        if(validate_if_contour_is_too_small(c)):
            continue

        M = cv2.moments(c)
        if(M["m00"] == 0.0):
            return (0, 0)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)

def validate_if_contour_is_too_small(c):
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    if (radius < 15):
        return True
    else:
        return False

def create_mask_for_color_detector(frame):
    edges = canny(frame, dilate_mask)
    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK, RADIUS_LIMITER_CHECK)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_rect_limiter(RECT_W_LIMITER, RECT_H_LIMITER)
    shapeDetector.set_radius_limiter(RADIUS_LIMITER, RAIDUS_POSITIVE)
    
    shape = shapeDetector.detect(edges)
    shape = shapeDetector.detect(shape.frameCnts)

    mask = cv2.bitwise_and(frame, frame, mask=shape.frameWithText)

    kernel = np.ones((9, 9), np.uint8)
    kernelerode = np.ones((9,9),np.uint8)
    
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10)))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10)))
    mask = cv2.erode(mask,kernelerode,iterations = 1)

    shape.set_frame(mask)

    return shape
