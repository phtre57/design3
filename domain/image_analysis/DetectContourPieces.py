import cv2

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.Canny import canny, dilate_mask

"""
from ShapeValidator import ShapeValidator
from ShapeDetector import ShapeDetector
from Canny import canny, dilate_mask, erode_mask
"""


def detect_contour_pieces(frame):
    frame = frame.copy()

    edges = canny(frame, dilate_mask)
    shapeDetector = ShapeDetector(True, True, True)
    shapeDetector.set_peri_limiter(150, 750)
    shapeDetector.set_rect_limiter(10, 10)
    shapeDetector.set_radius_limiter(90, True)
    shape = shapeDetector.detect(edges, False)

    shape = shapeDetector.detect(edges, True)

    shape.set_frame(edges)

    return shape



# frame = cv2.imread("../../image_samples/real_image/pieces.jpg")
# detect_contour_pieces(frame)

# cv2.imshow('EDGES', frame)
# cv2.waitKey()