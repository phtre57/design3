import cv2
import imutils

from domain.image_analysis.ShapeValidator import ShapeValidator
from domain.image_analysis.Shape import Shape

debug = False


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

    def detect(self, frame):
        frame = frame.copy()

        self.shapes = []

        cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if (len(cnts) <= 0):
            return None

        c = max(cnts, key=cv2.contourArea)

        frameWithText = frame.copy()
        frameCnts = frame.copy()

        shapes_with_approx = []

        for c in cnts:
            shape = "unidentified"
            peri = cv2.arcLength(c, True)
            if (self.peri_limiter):
                if (peri > self.peri_upper):
                    continue
                elif (peri < self.peri_lower):
                    continue

            if debug:
                print("Wave")
                print(peri)

            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            ((xRect, yRect), (wRect, hRect), angleRect) = cv2.minAreaRect(c)

            if (self.rect_limiter):
                if (abs(wRect) < self.w_rect_limit
                        or abs(hRect) < self.h_rect_limit):
                    continue

            if debug:
                print(wRect, hRect)

            ((x, y), radius) = cv2.minEnclosingCircle(c)
            # center = (round(int(x)), round(int(y)))

            if debug:
                print(radius)

                img = frameWithText.copy()
                cv2.circle(img, (round(x), round(y)), 3, [0, 0, 255])
                cv2.imshow("SHOW", img)
                cv2.waitKey()

            if (self.radius_limiter):
                if (self.radius_positive):
                    if (radius > self.radius_limit):
                        continue
                else:
                    if (radius < self.radius_limit):
                        continue

            shapeValidator = ShapeValidator()
            shape = shapeValidator.validate(approx)

            if (self.shape_only is not None):
                if (shape != self.shape_only):
                    continue

            self.shapes.append(shape)
            shapes_with_approx.append([shape, approx, c])

            cv2.drawContours(frameWithText, [c], -1, (70, 0, 255), 10)
            cv2.putText(frameWithText, shape,
                        (int(x - radius), int(y - radius)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70, 0, 255), 2)

            cv2.drawContours(frameCnts, [c], -1, (100, 0, 255), 1)

            filler = cv2.convexHull(c)
            cv2.fillConvexPoly(frameWithText, filler, 255)
            cv2.fillConvexPoly(frameCnts, filler, 255)

        return Shape(self.shapes, cnts, shapes_with_approx, frameWithText,
                     frameCnts)

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
