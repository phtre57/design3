import cv2
import pickle

from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from infrastructure.communication_pi.__comm_pi import Communication_pi

SHOW_IMAGE_CALIBRATION = True


def CalibrateWorldCam():
    with open('calibration_data.pkl', 'wb') as output:
        img = take_world_image()
        picklize(img, output, CHESS_SQUARE_WIDTH, NUMBER_OF_LINES,
                 NUMBER_OF_COLUMNS, False)


def CalibrateEmbarkCam(comm_pi):
    with open('calibration_embark.pkl', 'wb') as output:
        img = comm_pi.getImage()
        cv2.imwrite("embark_calib.jpg", img)
        cv2.imshow('DEBUG', img)
        cv2.waitKey()
        picklize(img, output, EMBARKED_CHESS_SQUARE_WIDTH,
                 EMBARK_NUMBER_OF_LINES, EMBARK_NUMBER_OF_COLUMNS, True)


def picklize(img, output, chess_square_width, number_of_lines,
             number_of_columns, embark):
    c = PixelToXYCoordinatesConverter(
        img,
        chess_square_width,
        number_of_lines,
        number_of_columns,
        SHOW_IMAGE_CALIBRATION,
        embark=embark)
    pickle.dump(c, output, pickle.HIGHEST_PROTOCOL)


def take_world_image():
    cap = cv2.VideoCapture(1)
    print("Capture d'image en cours...")
    ret, img = cap.read()
    cap.release()
    return img


comm_pi = Communication_pi()
comm_pi.connectToPi()
CalibrateEmbarkCam(comm_pi)

# CalibrateWorldCam()
