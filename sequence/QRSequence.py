import cv2

from domain.image_analysis.opencv_callable.DetectQR import *
from infrastructure.communication_ui.comm_ui import Communication_ui
from infrastructure.communication_ui.ui_destination import *

def try_to_decode_qr(img_embarked):
    dict_of_values = decode(img_embarked)
    piece_color = dict_of_values[COULEUR]
    piece_shape = dict_of_values[PIECE]
    depot_number = dict_of_values[ZONE]

    send_qr_to_ui(
        str(depot_number) + ' Couleur: ' + str(piece_color) + ' Forme: ' +
        str(piece_shape))

    logger.log_info("Values of qr code: " + str(dict_of_values))
    logger.log_info(("Value of piece_color: " + str(piece_color)))
    logger.log_info(("Value of piece_shape: " + str(piece_shape)))
    logger.log_info(("Value of depot_number: " + str(depot_number)))

    if dict_of_values is None:
        return None

    return {'zone': depot_number, 'color': piece_color, 'shape': piece_shape}


def send_qr_to_ui(string_qr):
    comm_ui = Communication_ui()
    comm_ui.SendText(string_qr, QR_CODE_TEXT())
