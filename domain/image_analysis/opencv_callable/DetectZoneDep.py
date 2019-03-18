import cv2

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, dilate_mask_zone_dep

PERI_LIMITER_CHECK = True
PERI_LIMITER_UPPER = 7000
PERI_LIMITER_LOWER = 600
RECT_LIMITER_CHECK = False
RADIUS_LIMITER_CHECK = True
RADIUS_LIMITER = 300
RAIDUS_POSITIVE = True
CHECK_SHAPE_ONLY = "rectangle"

def detect_zone_dep(frame):
    frame.copy()

    edges = canny(frame, dilate_mask_zone_dep)
    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK, RADIUS_LIMITER_CHECK)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_radius_limiter(RADIUS_LIMITER, RAIDUS_POSITIVE)
    shapeDetector.set_shape_only(CHECK_SHAPE_ONLY)
    
    shape = shapeDetector.detect(edges)
    shape = shapeDetector.detect(shape.frameCnts)
    shape.set_frame(shape.frameWithText)

    return shape