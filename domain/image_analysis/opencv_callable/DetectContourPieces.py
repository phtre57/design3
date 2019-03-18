import cv2

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, dilate_mask

def detect_contour_pieces(frame):
    frame = frame.copy()

    edges = canny(frame, dilate_mask)
    shapeDetector = ShapeDetector(True, True, True)
    shapeDetector.set_peri_limiter(150, 750)
    shapeDetector.set_rect_limiter(10, 10)
    shapeDetector.set_radius_limiter(90, True)
    
    shape = shapeDetector.detect(edges)
    shape = shapeDetector.detect(shape.frameCnts)
    shape.set_frame(shape.frameWithText)

    return shape