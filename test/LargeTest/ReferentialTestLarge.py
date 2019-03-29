import os
import time
from infrastructure.communication_pi.__comm_pi import *
from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *

def test():
    path2 = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
    path2 = os.path.normpath(os.path.join(path2, os.pardir))
    path2 = os.path.normpath(os.path.join(path2, os.pardir))
    path2 = os.path.join(path2, "./design3/image_samples/piece_xy/")
    img1 = cv2.imread(path2 + "piece_calib_3.jpg")
    small_converter = PixelToXYCoordinatesConverter(img1, EMBARKED_CHESS_SQUARE_WIDTH, 4, 4, False)

    comm = Communication_pi()
    comm.connectToPi()
    time.sleep(5)

    point = (5, 10)
    real_point = small_converter.convert_pixel_to_xy_point_given_angle(point, 0)
    x_coord = round(real_point[0])
    y_coord = round(real_point[1])
    print("Real point in mm: " + str(real_point))
    comm.sendCoordinates(str(x_coord) + "," + str(y_coord) + ",0" + "\n")

    input("Press enter:")

    real_point = small_converter.convert_pixel_to_xy_point_given_angle(point, 90)
    x_coord = round(real_point[0])
    y_coord = round(real_point[1])
    print("Real point in mm: " + str(real_point))
    comm.sendCoordinates(str(x_coord) + "," + str(y_coord) + ",0" + "\n")

    input("Press enter:")

    real_point = small_converter.convert_pixel_to_xy_point_given_angle(point, 180)
    x_coord = round(real_point[0])
    y_coord = round(real_point[1])
    print("Real point in mm: " + str(real_point))
    comm.sendCoordinates(str(x_coord) + "," + str(y_coord) + ",0" + "\n")

    input("Press enter:")

    real_point = small_converter.convert_pixel_to_xy_point_given_angle(point, -90)
    x_coord = round(real_point[0])
    y_coord = round(real_point[1])
    print("Real point in mm: " + str(real_point))
    comm.sendCoordinates(str(x_coord) + "," + str(y_coord) + ",0" + "\n")


test()