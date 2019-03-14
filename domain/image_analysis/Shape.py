class Shape:
    def __init__(self, shapes, cnts, approx, frameWithText, frameCnts):
        self.shapes = shapes
        self.cnts = cnts
        self.approx = approx
        self.frameWithText = frameWithText
        self.frameCnts = frameCnts
        self.frame = 0
        self.result = ""

    def set_frame(self, frame):
        self.frame = frame