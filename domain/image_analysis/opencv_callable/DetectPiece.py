from domain.image_analysis.opencv_callable.DetectContourPieces import detect_contour_pieces
from domain.image_analysis.opencv_callable.ColorDetector import color_detector
from util.color import Color
from util.Logger import Logger

logger = Logger(__name__)


def detect_piece(frame, str_shape, str_color, validation=False):
    logger.log_info('Detected piece got ' + str(str_shape) + " " +
                    str(str_color))
    frame = frame.copy()
    if (str_color is not None):
        color = Color()
        if (str_color == 'rouge'):
            color.RED()
        elif (str_color == 'bleu'):
            color.BLUE()
        elif (str_color == 'vert'):
            color.GREEN()
        elif (str_color == 'jaune'):
            color.YELLOW()
        elif (str_color == 'orange'):
            color.YELLOW()
        else:
            raise Exception('This color is not recognized')
        return color_detector(frame, color, validation=False)
    elif (str_shape is not None):
        return detect_contour_pieces(frame, str_shape, validation=False)
    else:
        logger.log_critical('Detect Piece, les params sont vraiment pas bon ' +
                            str(str_shape) + str(str_color))
