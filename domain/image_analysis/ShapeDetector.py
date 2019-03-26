import cv2
import imutils
import numpy as np

from domain.image_analysis.ShapeValidator import ShapeValidator
from domain.image_analysis.Shape import Shape
from context.config import SHAPE_DETECTOR_DEBUG

DEBUG = SHAPE_DETECTOR_DEBUG


class ShapeDetector:
    def __init__(self,
                 peri_limiter,
                 rect_limiter,
                 radius_limiter,
                 radius_large=False):
        self.shapes = []
        self.peri_limiter = peri_limiter
        self.peri_lower = 0
        self.peri_upper = 0
        self.rect_limiter = rect_limiter
        self.w_rect_limit = 0
        self.h_rect_limit = 0
        self.angle_limiter = False
        self.radius_limiter = radius_limiter
        self.radius_limit = 0
        self.radius_positive = True
        self.radius_large = radius_large
        self.radius_large_limit = 0
        self.shape_only = None
        self.w_rect_limit_up = None
        self.h_rect_limit_up = None
        self.comparator_cnts = None

    def detect(self, frame, og_frame):
        frame = frame.copy()

        self.shapes = []

        cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if DEBUG:
            frame1 = og_frame.copy()
            cv2.drawContours(frame1, cnts, -1, (0, 255, 0), 3)
            cv2.imshow('CNTS', frame1)
            cv2.waitKey()

        if (len(cnts) <= 0):
            return None

        c = max(cnts, key=cv2.contourArea)

        frameWithText = frame.copy()
        frameCnts = frame.copy()
        height, width = frame.shape
        frameClean = frame.copy()
        kernelerode = np.ones((8, 8), np.uint8)
        frameClean = cv2.erode(frameClean, kernelerode, iterations=6)

        shapes_with_approx = []

        for c in cnts:

            if DEBUG:
                frame1 = og_frame.copy()
                cv2.drawContours(frame1, c, -1, (0, 255, 0), 3)
                cv2.imshow('CNTS1', frame1)
                cv2.waitKey()

            if self.comparator_cnts is not None:
                dist = cv2.matchShapes(c, self.comparator_cnts, 1, 0)
                if DEBUG:
                    print('dist ', dist)

            shape = "unidentified"
            peri = cv2.arcLength(c, True)
            if DEBUG:
                print("Wave")
                print(peri)
                print('Upper peri', peri > self.peri_upper)
                print('Lower peri ', peri < self.peri_lower)

            if (self.peri_limiter):
                if (peri > self.peri_upper):
                    continue
                elif (peri < self.peri_lower):
                    continue

            if (self.shape_only is not None and self.shape_only == 'circle'):
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            else:
                approx = cv2.approxPolyDP(c, 0.05 * peri, True)

            ((xRect, yRect), (wRect, hRect), angleRect) = cv2.minAreaRect(c)

            if DEBUG:
                print(wRect, hRect, angleRect)
                print(self.w_rect_limit)
                print('W rect ', abs(wRect) < self.w_rect_limit)
                print('H rect ', abs(hRect) < self.h_rect_limit)
                if(self.w_rect_limit_up is not None):
                    print('W rect up ', abs(wRect) > self.w_rect_limit_up)
                    print('H rect up ', abs(hRect) > self.h_rect_limit_up)
                img = frameClean.copy()
                cv2.drawContours(img, c, -1, 255, 3)
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(img, [box], 0, 255, 2)
                filler = cv2.convexHull(c)
                cv2.fillConvexPoly(img, filler, 255)
                cv2.imshow('SHAPE CHOSEN RECT', img)
                cv2.waitKey()

            if (self.rect_limiter):
                # if (hRect > wRect):
                #     t = wRect
                #     wRect = hRect
                #     hRect = t
                if (abs(wRect) < self.w_rect_limit
                        or abs(hRect) < self.h_rect_limit):
                    continue
                if (self.w_rect_limit_up is not None
                        and self.h_rect_limit_up is not None
                        and (abs(wRect) > self.w_rect_limit_up
                             or abs(hRect) > self.h_rect_limit_up)):
                    continue

                if DEBUG:
                    print('Rect passed')
                    

            if (self.angle_limiter):
                if (abs(angleRect) > 80):
                    if (90 - abs(angleRect) > 8):
                        continue
                else:
                    if (90 - abs(angleRect) < 82):
                        continue

                if DEBUG:
                    print('Angle passed')

            ((x, y), radius) = cv2.minEnclosingCircle(c)
            # center = (round(int(x)), round(int(y)))

            if DEBUG:
                print(radius)

            if (self.radius_limiter):
                if (self.radius_positive):
                    if (radius > self.radius_limit):
                        continue
                else:
                    if (radius < self.radius_limit):
                        continue

                if DEBUG:
                    print('Radius passed')

            if (self.radius_large and radius > self.radius_large_limit):
                continue

            if DEBUG:
                img = frameClean.copy()
                cv2.drawContours(img, c, -1, 255, 3)
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(img, [box], 0, 255, 2)
                filler = cv2.convexHull(c)
                cv2.fillConvexPoly(img, filler, 255)
                cv2.imshow('SHAPE CHOSEN RADIUS', img)
                cv2.waitKey()

                frame2 = frame.copy()
                kernelerode = np.ones((8, 8), np.uint8)
                frame2 = cv2.erode(frame2, kernelerode, iterations=6)
                cv2.drawContours(frame2, c, -1, (0, 255, 0), 3)
                cv2.imshow('SHAPE CHOSEN RADIUS', frame2)
                cv2.waitKey()

            shapeValidator = ShapeValidator()
            shape = shapeValidator.validate(approx)

            if (self.shape_only is not None):
                if (shape != self.shape_only):
                    if (DEBUG):
                        print(len(approx))
                        print('SKIPPED NOT THE RIGHT SHAPE')
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
            cv2.fillConvexPoly(frameClean, filler, 255)

        return Shape(self.shapes, cnts, shapes_with_approx, frameWithText,
                     frameCnts, frameClean)

    def set_peri_limiter(self, peri_lower, peri_upper):
        self.peri_lower = peri_lower
        self.peri_upper = peri_upper

    def set_rect_limiter(self,
                         w_rect_limit,
                         h_rect_limit,
                         angle_limiter=None,
                         h_rect_limit_up=None,
                         w_rect_limit_up=None):
        self.w_rect_limit = w_rect_limit
        self.h_rect_limit = h_rect_limit
        self.angle_limiter = angle_limiter
        self.h_rect_limit_up = h_rect_limit_up
        self.w_rect_limit_up = w_rect_limit_up

    def set_radius_limiter(self, radius_limit, radius_positive):
        self.radius_limit = radius_limit
        self.radius_positive = radius_positive

    def set_shape_only(self, shape):
        self.shape_only = shape

    def set_radius_large_limit(self, radius_large_limit):
        self.radius_large_limit = radius_large_limit

    def set_comparator_shape(self, comparator_cnts):
        self.comparator_cnts = comparator_cnts
