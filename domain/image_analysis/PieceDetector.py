from domain.image_analysis.ShapeDetector import *

class PieceDetector:

    def __init__(self):
        self.shape_detector = ShapeDetector(True, True, True)

    def get_center_of_piece(self):
        print("Io")