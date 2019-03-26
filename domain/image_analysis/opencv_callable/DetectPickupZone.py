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
RECT_W_LIMITER = 85
RECT_H_LIMITER = 15
RECT_W_LIMITER_UP = 110
RECT_H_LIMITER_UP = 45
RADIUS_LIMITER_CHECK = True
RADIUS_LIMITER = 150
RAIDUS_POSITIVE = True
ANGLE_LIMITER = True

OFFSET_PATHFINDING = 40

DEBUG = DETECT_PICKUP_ZONE_DEBUG

logger = Logger(__name__)


def detect_pickup_zone(og_frame):
    frame = og_frame.copy()
    frame = frame.copy()
    IMG_HEIGHT, IMG_WIDTH, _ = frame.shape

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = cv2.convertScaleAbs(frame, alpha=2.5, beta=100)
    frame = cv2.convertScaleAbs(frame, alpha=1.0, beta=100)

    if DEBUG:
        cv2.imshow('gray', frame)
        cv2.waitKey()

    edges = canny(frame, erode_mask_zone_dep_world, 285, 250)

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

    vertical = edges.copy()
    rows = vertical.shape[0]
    verticalsize = round(rows / 30)
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,
                                                  (1, verticalsize))
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)
    edges = vertical

    if DEBUG:
        cv2.imshow('CANNY AFTER MASK', edges)
        cv2.waitKey()

    edges = cv2.dilate(
        edges,
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)),
        iterations=1)

    if DEBUG:
        cv2.imshow('CANNY AFTER MASK', edges)
        cv2.waitKey()

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
                cv2.fillConvexPoly(frame1, filler, 255)
                print(wRect, hRect)
                cv2.imshow('DEBUG CONTOUR', frame1)
                cv2.waitKey()

            if (abs(wRect) < RECT_W_LIMITER or abs(hRect) < RECT_H_LIMITER):
                continue
            if (abs(wRect) > RECT_W_LIMITER_UP
                    or abs(hRect) > RECT_H_LIMITER_UP):
                continue

            if DEBUG:
                frame1 = og_frame.copy()
                cv2.drawContours(frame1, new_c, -1, (0, 255, 0), 3)
                cv2.imshow('FOUND', frame1)
                cv2.waitKey()

            center = adjust_start_zone_offset((round(xRect), round(yRect)),
                                              wRect, hRect, IMG_HEIGHT)
            logger.log_debug('PICKUP ZONE - Found center ' + str(center[0]) +
                             ' ' + str(center[1]) + ' ' + center[2])

            return {'point': (center[0], center[1]), 'cardinal': center[2]}

    logger.log_debug('PICKUP ZONE - Fallback to upside down strategy')
    return detect_pickup_zone_the_other_side(og_frame)


def detect_pickup_zone_the_other_side(og_frame):
    frame = og_frame.copy()
    frame = frame.copy()
    IMG_HEIGHT, IMG_WIDTH, _ = frame.shape

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = cv2.convertScaleAbs(frame, alpha=2.5, beta=100)
    frame = cv2.convertScaleAbs(frame, alpha=2.0, beta=100)

    if DEBUG:
        cv2.imshow('gray', frame)
        cv2.waitKey()

    edges = canny(frame, erode_mask_zone_dep_world, 285, 250)

    edges = cv2.morphologyEx(
        edges, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)))

    edges = cv2.dilate(
        edges,
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        iterations=3)

    if DEBUG:
        cv2.imshow('CANNY', edges)
        cv2.waitKey()

    horizontal = edges.copy()
    cols = horizontal.shape[1]
    horizontal_size = round(cols / 30)
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,
                                                    (horizontal_size, 1))
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)
    edges = horizontal

    if DEBUG:
        cv2.imshow('CANNY AFTER MASK', edges)
        cv2.waitKey()

    edges = cv2.dilate(
        edges,
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)),
        iterations=1)

    if DEBUG:
        cv2.imshow('CANNY AFTER MASK', edges)
        cv2.waitKey()

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
                # frame1 = og_frame.copy()
                # frame1 = cv2.convertScaleAbs(frame1, alpha=0, beta=0)
                # filler = cv2.convexHull(new_k)
                # cv2.fillConvexPoly(frame1, filler, 255)
                # cv2.imshow('DEBUG CONTOUR', frame1)
                # cv2.waitKey()
                print('')

            # Flipped verification, it's normal
            if (abs(wRect) < RECT_H_LIMITER or abs(hRect) < RECT_W_LIMITER):
                continue
            if (abs(wRect) > RECT_H_LIMITER_UP
                    or abs(hRect) > RECT_W_LIMITER_UP):
                continue

            if DEBUG:
                frame1 = og_frame.copy()
                cv2.drawContours(frame1, new_c, -1, (0, 255, 0), 3)
                cv2.imshow('FOUND', frame1)
                cv2.waitKey()

            center = adjust_start_zone_offset_upside_down(
                (round(xRect), round(yRect)), wRect, hRect, IMG_WIDTH)
            logger.log_debug('PICKUP ZONE - Found center ' + str(center[0]) +
                             ' ' + str(center[1]) + ' ' + center[2])
            return {'point': (center[0], center[1]), 'cardinal': center[2]}

    logger.log_critical('PICKUP ZONE - Can\'t find pickup zone')
    raise Exception('Can\'t find pickup zone')


def adjust_start_zone_offset_upside_down(point, wRect, hRect, width):
    if (point[0] > width / 2):
        return (point[0] - OFFSET_PATHFINDING + round(wRect / 2), point[1],
                EAST())
    else:
        return (point[0] + OFFSET_PATHFINDING + round(wRect / 2),
                point[1] + round(hRect), WEST())


def adjust_start_zone_offset(point, wRect, hRect, height):
    # Faire les deux bords de la table avec un beau if
    if (point[1] > height / 2):
        return (point[0] + round(wRect),
                point[1] - OFFSET_PATHFINDING + round(hRect / 2), SOUTH())
    else:
        return (point[0], point[1] + OFFSET_PATHFINDING + round(hRect / 2),
                NORTH())
