import cv2

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.opencv_callable.Canny import canny, dilate_mask

PERI_LIMITER_CHECK = True
PERI_LIMITER_UPPER = 160
PERI_LIMITER_LOWER = 100
RECT_LIMITER_CHECK = True
RECT_W_LIMITER = 20
RECT_H_LIMITER = 20
RADIUS_LIMITER_CHECK = True
RADIUS_LIMITER = 90
RAIDUS_POSITIVE = True


def detect_contour_pieces(og_frame, str_shape):
    frame = og_frame.copy()
    frame = frame.copy()

    edges = canny(frame, dilate_mask)
    shapeDetector = ShapeDetector(PERI_LIMITER_CHECK, RECT_LIMITER_CHECK,
                                  RADIUS_LIMITER_CHECK)
    shapeDetector.set_peri_limiter(PERI_LIMITER_LOWER, PERI_LIMITER_UPPER)
    shapeDetector.set_rect_limiter(RECT_W_LIMITER, RECT_H_LIMITER)
    shapeDetector.set_radius_limiter(RADIUS_LIMITER, RAIDUS_POSITIVE)
    shapeDetector.set_shape_only(str_shape)

    shape = shapeDetector.detect(edges, og_frame.copy())
    shape.set_frame(shape.frameWithText)

    return shape