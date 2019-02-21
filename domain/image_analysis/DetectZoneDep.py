import cv2

from domain.image_analysis.ShapeDetector import ShapeDetector
from domain.image_analysis.Canny import canny, dilate_mask_zone_dep

"""
from ShapeValidator import ShapeValidator
from ShapeDetector import ShapeDetector
from Canny import canny, dilate_mask_zone_dep
"""

def detect_zone_dep(frame):
    edges = canny(frame, dilate_mask_zone_dep)
    shapeDetector = ShapeDetector(True, False, True)
    shapeDetector.set_peri_limiter(700, 7000)
    shapeDetector.set_radius_limiter(230, True)
    shape = shapeDetector.detect(edges, False)

    shape = shapeDetector.detect(edges, True)

    return shape


# frame = cv2.imread("../../image_samples/real_image/zonedep.jpg")
# detect_zone_dep(frame)
# cv2.imshow('EDGES', frame)

# cv2.waitKey()