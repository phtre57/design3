import cv2
import numpy as np

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import *
from domain.image_analysis.ShapeUtils import *
from context.config import DETECT_ZONE_DEP_WORLD_DEBUG
from domain.image_analysis.opencv_callable.ref_shape import ref
from util.Logger import Logger
from domain.image_analysis.Cardinal import *

PERI_LIMITER_CHECK = False
PERI_LIMITER_UPPER = 100000
PERI_LIMITER_LOWER = 150
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 60
RECT_H_LIMITER = 15
RECT_W_LIMITER_UP = 100
RECT_H_LIMITER_UP = 40
RADIUS_LIMITER_CHECK = False
RADIUS_LIMITER = 30
RAIDUS_POSITIVE = False

OFFSET_PATHFINDING_NORTH = 40
OFFSET_PATHFINDING_WEST = 40
OFFSET_PATHFINDING_SOUTH = 40
OFFSET_PATHFINDING_EAST = 40

DEBUG = DETECT_ZONE_DEP_WORLD_DEBUG

logger = Logger(__name__)


def detect_zone_dep_world(og_frame,
                          canny_down=110,
                          canny_up=150,
                          flipped=False):

    frame = og_frame.copy()
    frame = frame.copy()
    IMG_HEIGHT, IMG_WIDTH, _ = frame.shape

    edges = canny(frame, erode_mask_zone_dep_world, canny_down, canny_up)

    if (DEBUG):
        cv2.imshow('DEBUG', edges)
        cv2.waitKey()

    edges = cv2.morphologyEx(
        edges, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    kernelerode = np.ones((3, 3), np.uint8)
    edges = cv2.erode(edges, kernelerode, iterations=1)

    if (DEBUG):
        cv2.imshow('DEBUG', edges)
        cv2.waitKey()

    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK,
                                  RADIUS_LIMITER_CHECK)
    if (flipped):
        shapeDetector.set_rect_limiter(
            RECT_H_LIMITER,
            RECT_W_LIMITER,
            angle_limiter=None,
            h_rect_limit_up=RECT_W_LIMITER_UP,
            w_rect_limit_up=RECT_H_LIMITER_UP)
    else:
        shapeDetector.set_rect_limiter(
            RECT_W_LIMITER,
            RECT_H_LIMITER,
            angle_limiter=None,
            w_rect_limit_up=RECT_W_LIMITER_UP,
            h_rect_limit_up=RECT_H_LIMITER_UP)
    shape = shapeDetector.detect(edges, og_frame.copy())

    if DEBUG:
        for k in shape.approx:
            frame1 = og_frame.copy()
            cv2.drawContours(frame1, k[2], -1, (0, 255, 0), 3)
            cv2.imshow('DEBUG CNTS', frame1)
            cv2.waitKey()
        cv2.imshow('frameClean', shape.frameClean)
        cv2.waitKey()

    output = cv2.bitwise_and(frame, frame, mask=shape.frameClean)

    shape.set_frame(output)

    if (len(shape.approx) != 1):
        if (flipped):
            logger.log_critical(
                'ZONE DEPOT WORLD - Couldn\'nt find the zone depot world')
            raise Exception("Can't find zone depot world")
        if (canny_down == 70):
            logger.log_debug(
                'ZONE DEPOT WORLD - Fallback to lowest (10) bracket canny strategy'
            )
            return detect_zone_dep_world(og_frame, 10, 150)
        if (canny_down == 10):
            logger.log_debug(
                'ZONE DEPOT WORLD - Fallback to upper zone strategy')
            return detect_zone_dep_world(og_frame, 10, 150, True)
        logger.log_debug(
            'ZONE DEPOT WORLD - Fallback to lower (70) bracket canny strategy')
        return detect_zone_dep_world(og_frame, 70, 150)

    shape.center = find_center(shape.approx[0][2], 10, shape)

    if (flipped):
        center = adjust_start_zone_offset_upside_down(shape.center, IMG_WIDTH,
                                                      shape.approx[0][3])
        logger.log_debug('ZONE DEPOT WORLD - Found center ' + str(center[0]) +
                         ' ' + str(center[1]) + ' ' + center[2])
        return {'point': (center[0], center[1]), 'cardinal': center[2]}
    else:
        center = adjust_start_zone_offset(shape.center, IMG_HEIGHT,
                                          shape.approx[0][3])
        logger.log_debug('ZONE DEPOT WORLD - Found center ' + str(center[0]) +
                         ' ' + str(center[1]) + ' ' + center[2])

        return {'point': (center[0], center[1]), 'cardinal': center[2]}


def adjust_start_zone_offset_upside_down(point, width, w_h_rect):
    if (point[0] > width / 2):
        return (point[0] - OFFSET_PATHFINDING_EAST,
                point[1] - round(w_h_rect[1] / 2), EAST())
    else:
        return (point[0] + OFFSET_PATHFINDING_WEST,
                point[1] + round(w_h_rect[1] / 2), WEST())


def adjust_start_zone_offset(point, height, w_h_rect):
    # Faire les deux bords de la table avec un beau if
    if (point[1] > height / 2):
        return (point[0] + round(w_h_rect[0] / 2),
                point[1] - OFFSET_PATHFINDING_NORTH, SOUTH())
    else:
        return (point[0] - round(w_h_rect[0] / 2),
                point[1] + OFFSET_PATHFINDING_SOUTH, NORTH())
