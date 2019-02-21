import cv2
import imutils

from domain.image_analysis.ShapeValidator import ShapeValidator
from domain.image_analysis.Shape import Shape

class ShapeDetector:

    def __init__(self, peri_limiter, rect_limiter, radius_limiter):
        self.shapes = []
        self.peri_limiter = peri_limiter
        self.peri_lower = 0
        self.peri_upper = 0
        self.rect_limiter = rect_limiter
        self.w_rect_limit = 0
        self.h_rect_limit = 0
        self.radius_limiter = radius_limiter
        self.radius_limit = 0
        self.radius_positive = True
        self.shape_only = None

    # 700, 150, 0.02, 10, 10, 90, True
    def detect(self, frame, second):
        self.shapes = []

        cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if (len(cnts) <= 0):
            return None

        c = max(cnts, key=cv2.contourArea)

        for c in cnts:
            shape = "unidentified"
            peri = cv2.arcLength(c, True)

            if (self.peri_limiter):
                if (peri > self.peri_upper):
                    continue
                elif (peri < self.peri_lower):
                    continue

            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            ((xRect, yRect), (wRect, hRect), angleRect) = cv2.minAreaRect(c)

            if (self.rect_limiter):
                if (abs(wRect) < self.w_rect_limit or abs(hRect) < self.h_rect_limit):
                    continue


            ((x, y), radius) = cv2.minEnclosingCircle(c)
            center = (round(int(x)),round(int(y)))

            if (self.radius_limiter):
                if (self.radius_positive):
                    if (radius > self.radius_limit):
                        continue
                else:
                    if (radius < self.radius_limit):
                        continue


            shapeValidator = ShapeValidator()
            shape = shapeValidator.validate(approx)

            if (self.shape_only != None):
                if (shape != self.shape_only):
                    continue
                    
            self.shapes.append(shape)

            if (second):
                cv2.drawContours(frame, [c], -1, (70,0,255), 10)
                cv2.putText(frame, shape, (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (70, 0, 255), 2)
            else:
                cv2.drawContours(frame, [c], -1, (100,0,255), 1)

            filler = cv2.convexHull(c)
            cv2.fillConvexPoly(frame, filler, 255)
            
        return Shape(self.shapes, cnts, approx)

    def set_peri_limiter(self, peri_lower, peri_upper):
        self.peri_lower = peri_lower
        self.peri_upper = peri_upper

    def set_rect_limiter(self, w_rect_limit, h_rect_limit):
        self.w_rect_limit = w_rect_limit
        self.h_rect_limit = h_rect_limit

    def set_radius_limiter(self, radius_limit, radius_positive):
        self.radius_limit = radius_limit
        self.radius_positive = radius_positive

    def set_shape_only(self, shape):
        self.shape_only = shape

    # 100000, 1000, 0.02, 90, 90, 100, False
    # def detectTable(self, frame, second):
        
    # 1500, 0, 0.02, 90, 90, 100, False
    # def detectStart(self, frame, second):
        
    # 1500, 0, 0.02, 90, 90, 100, False
    # def detectObstacle(self, frame, second):