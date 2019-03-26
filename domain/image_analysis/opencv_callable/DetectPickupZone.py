import cv2
import numpy as np
import imutils

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import *
from domain.image_analysis.ShapeUtils import *
from util.Logger import Logger
from context.config import DETECT_PICKUP_ZONE_DEBUG

PERI_LIMITER_CHECK = False
PERI_LIMITER_UPPER = 100000
PERI_LIMITER_LOWER = 150
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 60
RECT_H_LIMITER = 15
RECT_W_LIMITER_UP = 100
RECT_H_LIMITER_UP = 40
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
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,
                                                  (1, verticalsize))
    # Apply morphology operations
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)
    edges = vertical

    if DEBUG:
        cv2.imshow('CANNY AFTER MASK', edges)
        cv2.waitKey()

    # horizontal = edges.copy()
    # cols = horizontal.shape[1]
    # horizontal_size = round(cols / 30)
    # # Create structure element for extracting horizontal lines through morphology operations
    # horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,
    #                                                 (horizontal_size, 1))
    # # Apply morphology operations
    # horizontal = cv2.erode(horizontal, horizontalStructure)
    # horizontal = cv2.dilate(horizontal, horizontalStructure)
    # edges2 = horizontal

    # if DEBUG:
    #     cv2.imshow('CANNY AFTER MASK', edges2)
    #     cv2.waitKey()

    # edges = cv2.addWeighted(edges2, 1, edges1, 1, 0.0)

    # edges = cv2.bitwise_and(edges2, edges2, mask=edges1)

    edges = cv2.dilate(
        edges,
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10)),
        iterations=1)

    # kernelerode = np.ones((2, 2), np.uint8)
    # edges = cv2.erode(edges, kernelerode, iterations=1)

    if DEBUG:
        cv2.imshow('CANNY AFTER MASK', edges)
        cv2.waitKey()

    cnts = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
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

            ((xRect, yRect), (wRect, hRect), angleRect) = cv2.minAreaRect(new_k)
            
            if DEBUG:
                # frame1 = og_frame.copy()
                # frame1 = cv2.convertScaleAbs(frame1, alpha=0, beta=0)
                # filler = cv2.convexHull(new_k)
                # cv2.fillConvexPoly(frame1, filler, 255)
                # cv2.imshow('DEBUG CONTOUR', frame1)
                # cv2.waitKey()
                print('')

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
            
            return adjust_start_zone_offset((round(xRect), round(yRect)))
    
    return detect_pickup_zone_the_other_side(og_frame)

def detect_pickup_zone_the_other_side(og_frame):
    frame = og_frame.copy()
    frame = frame.copy()

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
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,
                                                    (horizontal_size, 1))
    # Apply morphology operations
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

    cnts = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
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

            ((xRect, yRect), (wRect, hRect), angleRect) = cv2.minAreaRect(new_k)
            
            if DEBUG:
                # frame1 = og_frame.copy()
                # frame1 = cv2.convertScaleAbs(frame1, alpha=0, beta=0)
                # filler = cv2.convexHull(new_k)
                # cv2.fillConvexPoly(frame1, filler, 255)
                # cv2.imshow('DEBUG CONTOUR', frame1)
                # cv2.waitKey()
                print('')

            # Flipped verification, it's normal
            if (abs(wRect) < RECT_H_LIMITER
                or abs(hRect) < RECT_W_LIMITER):
                continue
            if (abs(wRect) > RECT_H_LIMITER_UP
                    or abs(hRect) > RECT_W_LIMITER_UP):
                continue

            if DEBUG:
                frame1 = og_frame.copy()
                cv2.drawContours(frame1, new_c, -1, (0, 255, 0), 3)
                cv2.imshow('FOUND', frame1)
                cv2.waitKey()
            
            return adjust_start_zone_offset_upside_down((round(xRect), round(yRect)))

    logger.log_critical('PICKUP ZONE - Can\'t find pickup zone')
    raise Exception('Can\'t find pickup zone')

def adjust_start_zone_offset_upside_down(point):
    if (point[0] > 320/2):
        return (point[0] - OFFSET_PATHFINDING, point[1])
    else:
        return (point[0] + OFFSET_PATHFINDING, point[1])

def adjust_start_zone_offset(point):
    # Faire les deux bords de la table avec un beau if
    if (point[1] > 120):
        return (point[0], point[1] - OFFSET_PATHFINDING)
    else:
        return (point[0], point[1] + OFFSET_PATHFINDING)
