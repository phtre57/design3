from domain.image_analysis.opencv_callable.DetectContourPieces import detect_contour_pieces
from domain.image_analysis.opencv_callable.ColorDetector import color_detector
from util.color import Color
from util.Logger import Logger

logger = Logger(__name__)


def detect_piece(frame, str_shape, str_color):
    if (str_color is not None):
        color = Color()
        if (str_color == 'rouge'):
            color.RED()
        elif (str_color == 'bleu'):
            color.BLUE()
        elif (str_color == 'vert'):
            color.GREEN()
        else:
            color.YELLOW()
        return color_detector(frame, color)
    elif (str_shape is not None):
        return detect_contour_pieces(frame, str_shape)
    else:
        logger.log_critical('Detect Piece, les params sont vraiment pas bon ' + str(str_shape) + str(str_color))
