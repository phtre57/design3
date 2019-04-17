import cv2
import numpy as np
import imutils

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import *
from domain.image_analysis.ShapeUtils import *
from util.Logger import Logger
from context.config import DETECT_PICKUP_ZONE_DEBUG
from domain.image_analysis.Cardinal import *

PERI_LIMITER_CHECK = False
PERI_LIMITER_UPPER = 100000
PERI_LIMITER_LOWER = 150
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 82
RECT_H_LIMITER = 25
RECT_W_LIMITER_UP = 95
RECT_H_LIMITER_UP = 42
RADIUS_LIMITER_CHECK = True
RADIUS_LIMITER = 150
RAIDUS_POSITIVE = True
ANGLE_LIMITER = True

OFFSET_PATHFINDING_NORTH = 40
OFFSET_PATHFINDING_WEST = 40
OFFSET_PATHFINDING_SOUTH = 40
OFFSET_PATHFINDING_EAST = 40

DEBUG = DETECT_PICKUP_ZONE_DEBUG

logger = Logger(__name__)


def detect_pickup_zone(og_frame):
    frame = og_frame.copy()
    frame = frame.copy()
    IMG_HEIGHT, IMG_WIDTH, _ = frame.shape

    edges = __setup_image_and_canny(frame, 1.0)

    vertical = edges.copy()
    rows = vertical.shape[0]
    vertical_size = (1, round(rows / 30))
    edges = __vertical_or_horizontal_lines_mask(vertical, vertical_size)

    resp = __find_and_analyse_every_contour(edges, adjust_start_zone_offset,
                                            IMG_HEIGHT, og_frame, False)

    if (resp['cardinal'] is None):
        logger.log_debug('PICKUP ZONE - Fallback to upside down strategy')
        return detect_pickup_zone_the_other_side(og_frame)

    return resp


def detect_pickup_zone_the_other_side(og_frame):
    frame = og_frame.copy()
    frame = frame.copy()
    IMG_HEIGHT, IMG_WIDTH, _ = frame.shape

    edges = __setup_image_and_canny(frame, 1.0)

    horizontal = edges.copy()
    cols = horizontal.shape[1]
    horizontal_size = (round(cols / 30), 1)
    edges = __vertical_or_horizontal_lines_mask(horizontal, horizontal_size)

    resp = __find_and_analyse_every_contour(
        edges, adjust_start_zone_offset_upside_down, IMG_WIDTH, og_frame, True)

    if (resp['cardinal'] is None):
        logger.log_critical('PICKUP ZONE - Can\'t find pickup zone')
        raise Exception('Can\'t find pickup zone')

    return resp


def __setup_image_and_canny(frame, alpha):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=100)
    frame = cv2.convertScaleAbs(frame, alpha=1.0, beta=30)

    if DEBUG:
        cv2.imshow('gray', frame)
        cv2.waitKey()

    edges = canny(frame, erode_mask_zone_dep_world, 275, 250)

    if DEBUG:
        cv2.imshow('CANNY', edges)
        cv2.waitKey()

    edges = cv2.morphologyEx(
        edges, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)))

    edges = cv2.dilate(
        edges,
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        iterations=2)

    if DEBUG:
        cv2.imshow('CANNY', edges)
        cv2.waitKey()

    return edges


def __vertical_or_horizontal_lines_mask(vertical, size):

    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, size)
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)

    vertical = cv2.dilate(
        vertical,
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)),
        iterations=1)

    if DEBUG:
        cv2.imshow('CANNY AFTER MASK', vertical)
        cv2.waitKey()

    return vertical


def __find_and_analyse_every_contour(edges, adjust_offset_func,
                                     width_or_height, og_frame, flipped):
    cnts = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    for c in cnts:
        for cc in cnts:
            new_c = []
            for e in c:
                new_c.append(e)
            for e in cc:
                new_c.append(e)

            new_k = np.concatenate((c, cc))

            xRect, yRect, wRect, hRect = cv2.boundingRect(new_k)

            if DEBUG:
                frame1 = og_frame.copy()
                frame1 = cv2.convertScaleAbs(frame1, alpha=0, beta=0)
                filler = cv2.convexHull(new_k)
                print(xRect, yRect, wRect, hRect)
                cv2.fillConvexPoly(frame1, filler, 255)
                cv2.imshow('DEBUG CONTOUR', frame1)
                cv2.waitKey()

            if flipped:
                # Flipped verification, it's normal
                if xRect < 450:
                    continue
                if (abs(wRect) < RECT_H_LIMITER
                        or abs(hRect) < RECT_W_LIMITER):
                    continue
                if (abs(wRect) > RECT_H_LIMITER_UP
                        or abs(hRect) > RECT_W_LIMITER_UP):
                    continue
            else:
                if yRect < 300 and yRect > 100:
                    continue
                if (abs(wRect) < RECT_W_LIMITER
                        or abs(hRect) < RECT_H_LIMITER):
                    continue
                if (abs(wRect) > RECT_W_LIMITER_UP
                        or abs(hRect) > RECT_H_LIMITER_UP):
                    continue

            if DEBUG:
                frame1 = og_frame.copy()
                cv2.drawContours(frame1, new_c, -1, (0, 255, 0), 3)
                cv2.imshow('FOUND', frame1)
                cv2.waitKey()

            center = adjust_offset_func((round(xRect), round(yRect)), wRect,
                                        hRect, width_or_height)
            logger.log_debug('PICKUP ZONE - Found center ' + str(center[0]) +
                             ' ' + str(center[1]) + ' ' + center[2])

            return {'point': (center[0], center[1]), 'cardinal': center[2]}

    return {'point': (0, 0), 'cardinal': None}


def adjust_start_zone_offset_upside_down(point, wRect, hRect, width):
    if (point[0] > width / 2):
        return (point[0] - OFFSET_PATHFINDING_EAST + round(wRect / 2),
                point[1] - 15, EAST())
    else:
        return (point[0] + OFFSET_PATHFINDING_WEST + round(wRect / 2),
                point[1] + round(hRect) + 15, WEST())


def adjust_start_zone_offset(point, wRect, hRect, height):
    if (point[1] > height / 2):
        return (point[0] + round(wRect) + 15,
                point[1] - OFFSET_PATHFINDING_SOUTH + round(hRect / 2),
                SOUTH())
    else:
        return (point[0] - 15,
                point[1] + OFFSET_PATHFINDING_NORTH + round(hRect / 2),
                NORTH())
