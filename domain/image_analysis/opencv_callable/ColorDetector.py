import cv2
import numpy as np
import imutils

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

def color_detector(frame):
    frame = frame.copy()
    
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

