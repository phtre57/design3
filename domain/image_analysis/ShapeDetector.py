import cv2
import imutils

from ShapeValidator import ShapeValidator

class ShapeDetector:

    def __init__(self):
        self.shapes = []

    # 700, 150, 0.02, 10, 10, 90, True
    def detect(self, frame, second, peri_upper, peri_lower, peri_factor, w_rect_limit, h_rect_limit, radius_limit, radius_positive):
        self.shapes = []

        # cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
        #                             cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        for c in cnts:
            shape = "unidentified"
            peri = cv2.arcLength(c, True)

            if (peri > peri_upper):
                continue
            elif (peri < peri_lower):
                continue
            
            approx = cv2.approxPolyDP(c, peri_factor * peri, True)

            ((xRect, yRect), (wRect, hRect), angleRect) = cv2.minAreaRect(c)
            if (abs(wRect) < w_rect_limit or abs(hRect) < h_rect_limit):
                continue

            ((x, y), radius) = cv2.minEnclosingCircle(c)
            center = (round(int(x)),round(int(y)))

            if (radius_positive):
                if (radius > radius_limit):
                    continue
            else:
                if (radius < radius_limit):
                    continue

            shapeValidator = ShapeValidator()
            shape = shapeValidator.validate(approx)
            self.shapes.append(shape)

            if (second):
                cv2.drawContours(frame, [c], -1, (70,0,255), 10)
                cv2.putText(frame, shape, (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (70, 0, 255), 2)
            else:
                cv2.drawContours(frame, [c], -1, (100,0,255), 1)

            filler = cv2.convexHull(c)
            cv2.fillConvexPoly(frame, filler, 255)
            
            
        return self.shapes

    # 100000, 1000, 0.02, 90, 90, 100, False
    # def detectTable(self, frame, second):
        
    # 1500, 0, 0.02, 90, 90, 100, False
    # def detectStart(self, frame, second):
        
    # 1500, 0, 0.02, 90, 90, 100, False
    # def detectObstacle(self, frame, second):
        