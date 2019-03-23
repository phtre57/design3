import cv2

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, dilate_mask

PERI_LIMITER_CHECK = True
PERI_LIMITER_UPPER = 750
PERI_LIMITER_LOWER = 150
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 10
RECT_H_LIMITER = 10
RADIUS_LIMITER_CHECK = True
RADIUS_LIMITER = 90
RAIDUS_POSITIVE = True

def detect_contour_pieces(og_frame):
    frame = og_frame.copy()
    frame = frame.copy()

    edges = canny(frame, dilate_mask)
    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK, RADIUS_LIMITER_CHECK)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_rect_limiter(RECT_W_LIMITER, RECT_H_LIMITER)
    shapeDetector.set_radius_limiter(RADIUS_LIMITER, RAIDUS_POSITIVE)
    
    shape = shapeDetector.detect(edges, og_frame.copy())
    shape = shapeDetector.detect(shape.frameCnts, og_frame.copy())
    shape.set_frame(shape.frameWithText)

    return shape