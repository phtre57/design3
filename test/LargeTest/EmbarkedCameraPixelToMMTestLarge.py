import os
import unittest
from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from domain.image_analysis.ShapeDetector import *
from domain.image_analysis.opencv_callable.Canny import *
from sequence.SequencePiece import *

DEBUG = True


class EmbarkedCameraPixelToMMTestLarge(unittest.TestCase):

    def __calculate_xy_from_center_of_image(self, x, y, height, width):
        return x - width/2, y - height/2

    def setUp(self):
        self.path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.normpath(os.path.join(self.path, os.pardir))
        self.path = os.path.join(self.path, "./design3/image_samples/piece_xy/")
        img = cv2.imread(self.path + "piece_calib_3.jpg")
        self.embarkConverter = PixelToXYCoordinatesConverter(img, EMBARKED_CHESS_SQUARE_WIDTH, 4, 4, False)
        self.sequencePiece = SequencePiece(self.embarkConverter)

    def test_givenImageWithSquarexyPiece_whenFindingPiece_thenXYinMMReturned(self):
        if DEBUG:
            print("Square xy: ")

        frame = cv2.imread(self.path + "piece_xy.jpg")
        self.sequencePiece.find_position_of_wanted_piece_in_image(frame, "square")

    def test_givenImageWithBluePentagonxy7Piece_whenFindingPiece_thenXYinMMReturned(self):
        if DEBUG:
            print("Pentagon xy7: ")

        frame = cv2.imread(self.path + "piece_xy7.jpg")
        self.sequencePiece.find_position_of_wanted_piece_in_image(frame, "pentagon")

    def test_givenImageWithGreenTrianglexy2Piece_whenFindingPiece_thenXYinMMReturned(self):
        if DEBUG:
            print("Triangle xy2: ")

        frame = cv2.imread(self.path + "piece_xy2.jpg")
        self.sequencePiece.find_position_of_wanted_piece_in_image(frame, "triangle")

    def test_givenImageWithBluePentagonxy2Piece_whenFindingPiece_thenXYinMMReturned(self):
        if DEBUG:
            print("Pentagon xy2: ")

        frame = cv2.imread(self.path + "piece_xy2.jpg")
        self.sequencePiece.find_position_of_wanted_piece_in_image(frame, "pentagon")

    def test_givenImageWithGreenCirclexy2Piece_whenFindingPiece_thenXYinMMReturned(self):
        if DEBUG:
            print("Circle xy10: ")

        frame = cv2.imread(self.path + "piece_xy10.jpg")
        self.sequencePiece.find_position_of_wanted_piece_in_image(frame, "circle")



