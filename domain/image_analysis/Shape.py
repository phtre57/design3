class Shape:
    def __init__(self, shapes, cnts, approx, frameWithText, frameCnts, frameClean):
        self.shapes = shapes
        self.cnts = cnts
        self.approx = approx
        self.frameWithText = frameWithText
        self.frameCnts = frameCnts
        self.frame = 0
        self.result = ""
        self.center = (0, 0)
        self.frameClean = frameClean

    def set_frame(self, frame):
        self.frame = frame