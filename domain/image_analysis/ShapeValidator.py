import cv2


class ShapeValidator:

    def __init__(self):
        self.shape = ""

    def validate(self, cnts):
        if len(cnts) == 3:
            self.shape = "triangle"
        elif len(cnts) == 4:
            (x, y, w, h) = cv2.boundingRect(cnts)
            ar = w / float(h)
            self.shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        elif len(cnts) == 5:
            self.shape = "pentagon"
        else:
            self.shape = "circle"
        return self.shape