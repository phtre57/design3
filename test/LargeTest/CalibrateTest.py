import cv2
import pickle

from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *

cap = cv2.VideoCapture(1)


def take_image():
    print("Capture d'image en cours...")
    ret, img = cap.read()
    return img


with open('calibration_data.pkl', 'wb') as output:
    img = take_image()
    c = PixelToXYCoordinatesConverter(img, CHESS_SQUARE_WIDTH, NUMBER_OF_LINES,
                                      NUMBER_OF_COLUMNS)
    pickle.dump(c, output, pickle.HIGHEST_PROTOCOL)

# del company1
# del company2

# with open('calibration_data.pkl', 'rb') as input:
#     c = pickle.load(input)