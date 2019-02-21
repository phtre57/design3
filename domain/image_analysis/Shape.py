class Shape:
    def __init__(self, shapes, cnts, approx):
        self.shapes =  shapes
        self.cnts = cnts
        self.approx = approx
        self.frame = 0

    def set_frame(self, frame):
        self.frame = frame