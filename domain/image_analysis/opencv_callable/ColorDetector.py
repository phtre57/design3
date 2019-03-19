import cv2

from util.color import Color
from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, dilate_mask
from domain.image_analysis.ShapeUtils import *

RADIUS_LIMIT = 15

def color_detector(frame, color):
    frame = frame.copy()

    shape = create_mask_for_color_detector(frame)    

    res_contour = find_where_the_shape_is(shape, color, RADIUS_LIMIT)
    shape.res_contour = res_contour
    return shape

def create_mask_for_color_detector(frame):
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
