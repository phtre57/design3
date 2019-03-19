import cv2


class ShapeValidator:

    def __init__(self):
        self.shape = ""

    def validate(self, cnts):
        if len(cnts) == 3:
            self.shape = "triangle"
        elif len(cnts) == 4:
            rect = cv2.minAreaRect(cnts)
            (x, y), (w, h), angle = rect
            ar = w / float(h)
            self.shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        elif len(cnts) == 5:
            self.shape = "pentagon"
        else:
            self.shape = "circle"
        return self.shape