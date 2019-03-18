import cv2

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, dilate_mask_zone_dep

# WIP

def detect_zone_dep(frame):
    frame.copy()

    edges = canny(frame, dilate_mask_zone_dep)
    shapeDetector = ShapeDetector(True, False, True)
    shapeDetector.set_peri_limiter(700, 7000)
    shapeDetector.set_radius_limiter(230, True)
    
    shape = shapeDetector.detect(edges)
    shape = shapeDetector.detect(shape.frameCnts)
    shape.set_frame(shape.frameWithText)

    return shape