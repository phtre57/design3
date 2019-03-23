import cv2
import numpy as np

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import *
from domain.image_analysis.ShapeUtils import *

PERI_LIMITER_CHECK = False
PERI_LIMITER_UPPER = 100000
PERI_LIMITER_LOWER = 150
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 70
RECT_H_LIMITER = 15
RADIUS_LIMITER_CHECK = True
RADIUS_LIMITER = 150
RAIDUS_POSITIVE = True
ANGLE_LIMITER = True

DEBUG = False

def detect_pickup_zone(og_frame, second_try = False):
    frame = og_frame.copy()
    frame = frame.copy()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.convertScaleAbs(frame, alpha=3, beta=100)

    if (second_try):
        frame = cv2.convertScaleAbs(frame, alpha=1.1, beta=10)

    if DEBUG:
        cv2.imshow('gray', frame)
        cv2.waitKey()

    # edges = canny(frame, erode_mask_zone_dep_world, 245, 250)

    edges = canny(frame, erode_mask_zone_dep_world, 245, 285)

    if DEBUG:
        cv2.imshow('CANNY', edges)
        cv2.waitKey()

    edges = cv2.morphologyEx(
        edges, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)))

    vertical = edges.copy()
    rows = vertical.shape[0]
    verticalsize = round(rows / 30)
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
    # Apply morphology operations
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)
    edges1 = vertical

    if DEBUG:
        cv2.imshow('CANNY AFTER MASK', edges1)
        cv2.waitKey()

    horizontal = edges.copy()
    cols = horizontal.shape[1]
    horizontal_size = round(cols / 30)
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    # Apply morphology operations
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)
    edges2 = horizontal

    if DEBUG:
        cv2.imshow('CANNY AFTER MASK', edges2)
        cv2.waitKey()
        
    edges = cv2.addWeighted(edges2, 1, edges1, 1, 0.0)
    
    # edges = cv2.bitwise_and(edges2, edges2, mask=edges1)

    if DEBUG:
        cv2.imshow('CANNY', edges)
        cv2.waitKey()

    edges = cv2.dilate(
        edges,
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)),
        iterations=1)

    edges = cv2.erode(edges, kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)), iterations=1)


    # kernelerode = np.ones((2, 2), np.uint8)
    # edges = cv2.erode(edges, kernelerode, iterations=1)

    if DEBUG:
        cv2.imshow('CANNY AFTER MASK', edges)
        cv2.waitKey()

    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK,
                                  RADIUS_LIMITER_CHECK, True)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_rect_limiter(RECT_W_LIMITER, RECT_H_LIMITER, ANGLE_LIMITER)
    shapeDetector.set_radius_limiter(RADIUS_LIMITER, RAIDUS_POSITIVE)
    shapeDetector.set_radius_large_limit(60)

    shape = shapeDetector.detect(edges, og_frame.copy())

    if DEBUG:
        cv2.imshow('frameClean', shape.frameClean)
        cv2.waitKey()

    output = cv2.bitwise_and(frame, frame, mask=shape.frameClean)

    shape.set_frame(output)

    if (len(shape.approx) > 1 or len(shape.approx) == 0):
        if (not second_try):
            return detect_pickup_zone(og_frame, True)
        raise Exception("Can't find zone depot " + str(len(shape.approx)))

    shape.center = find_center(shape.approx[0][2], 10)
    shape.center = adjust_start_zone_offset(shape.center)

    cv2.circle(shape.frame, (shape.center[0], shape.center[1]), 1,
               [255, 51, 51])

    return shape


def adjust_start_zone_offset(point):
    # Faire les deux bords de la table avec un beau if
    if (point[1] > 120):
        return (point[0], point[1] - 35)
    else:
        return (point[0], point[1] + 35)
