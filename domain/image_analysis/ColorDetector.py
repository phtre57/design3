import cv2
import numpy as np
import imutils

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.Canny import canny, dilate_mask

def color_detector(frame):
    frame = frame.copy()
    
    edges = canny(frame, dilate_mask)
    shapeDetector = ShapeDetector(True, True, True)
    shapeDetector.set_peri_limiter(150, 700)
    shapeDetector.set_rect_limiter(10, 10)
    shapeDetector.set_radius_limiter(90, True)
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

