import time
import pickle
import sys
import traceback

from domain.pathfinding.Astar import Astar
from domain.pathfinding.PathSmoother import PathSmoother
from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from domain.image_analysis.ImageToGridConverter import *
from infrastructure.communication_pi.comm_pi import Communication_pi
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector

X_END_CHARGE = 35
Y_END_CHARGE = 170

X_END_QR = 265
Y_END_QR = 170

X_END_PICKUP = 179
Y_END_PICKUP = 78

X_END_DEPOT = 131
Y_END_DEPOT = 164

X_END_START = 81
Y_END_START = 121

X_END_TEST = 40
Y_END_TEST = 81

# X_END_TEST = 105
# Y_END_TEST = 121

cap = cv2.VideoCapture(1)
comm_pi = Communication_pi()

def move_robot(X_END, Y_END):
    img = take_image()

    robot_detector = RobotDetector(img)
    x_start, y_start = robot_detector.find_center_of_robot()

    grid_converter = ImageToGridConverter(img, x_start, y_start, X_END, Y_END)

    astar = Astar(grid_converter.grid, HEIGHT, LENGTH)

    path = astar.find_path()

    path_smoother = PathSmoother(path)
    smooth_path = path_smoother.smooth_path()

    for point in smooth_path:
        cv2.circle(grid_converter.image, (point[0], point[1]), 1, [0, 0, 255])

    cv2.imshow("path", grid_converter.image)
    cv2.waitKey(0)

    return smooth_path

def connect_and_calibrate():
    #connect to pi
    print("Now connecting...")
    comm_pi.connectToPi()
    time.sleep(5)

    #calibration phase
    print("Calibration phase: ")

    with open('calibration_data.pkl', 'rb') as input:
        pixel_to_xy_converter = pickle.load(input)
    
    #moving robot phase
    print("Starting path finding")

    return pixel_to_xy_converter

def test_main_loop_move_robot(X_END, Y_END):
    ok = True

    while ok:
        try:
            smooth_path = move_robot(X_END, Y_END)            

            ok = False
        except Exception as ex:
            print(ex)
            traceback.print_exc(file=sys.stdout)

    # Rotating robot to 0 degree
    print("Rotating robot phase: ")
    ok = True

    while ok:
        try:
            img = take_image()

            robot_detector = RobotDetector(img)
            robot_angle = robot_detector.find_angle_of_robot()
            turning_angle = int(round(robot_angle))

            print("Sending angle: " + "0,0," + str(turning_angle) + "\n")

            comm_pi.sendCoordinates("0,0," + str(turning_angle) + "\n")
            # time.sleep(10)

            ok = False
        except Exception as ex:
            print(ex)
            traceback.print_exc(file=sys.stdout)


    real_path = pixel_to_xy_converter.convert_to_xy(smooth_path)
    starting_point = real_path[0]
    real_path = real_path[1:]

    #send coords here
    for point in real_path:
        ok = True

        while ok:
            try:
                img = take_image(smooth_path)

                robot_detector = RobotDetector(img)
                robot_angle = robot_detector.find_angle_of_robot()
                turning_angle = int(round(robot_angle))

                print("Sending angle: " + "0,0," + str(turning_angle) + "\n")
                
                comm_pi.sendCoordinates("0,0," + str(turning_angle) + "\n")
                # time.sleep(2)

                ok = False
            except Exception as ex:
                print(ex)
                traceback.print_exc(file=sys.stdout)

        x_coord = int(round(point[0] - starting_point[0], 0))
        y_coord = int(round(point[1] - starting_point[1], 0))

        print("Sending coordinates: " + str(x_coord) + "," + str(y_coord) + ",0")

        comm_pi.sendCoordinates(str(x_coord) + "," + str(y_coord) + ",0" + "\n")
        # time.sleep(2)

        ok = True

        while ok:
            try:
                img = take_image(smooth_path)
                robot_detector = RobotDetector(img)
                x_new, y_new = robot_detector.find_center_of_robot()
                temp = (x_new, y_new)
                starting_point = pixel_to_xy_converter.convert_to_xy_point(temp)

                ok = False
            except Exception as ex:
                print(ex)
                traceback.print_exc(file=sys.stdout)


def take_image(smooth_path = None):
    print("Capture d'image en cours...")
    ret, img = cap.read()
    #cap.release()

    if (smooth_path is not None):
        for point in smooth_path:
            cv2.circle(img, (point[0]*2, point[1]*2), 1, [0, 0, 255])

    # cv2.imshow("imageCourante", img)
    # cv2.waitKey()

    cv2.destroyAllWindows()

    return img

X_CENTER = 159
Y_CENTER = 116

Y_POINT = 116
X_1 = 126
X_2 = 110
X_3 = 96
X_4 = 81
X_5 = 66
X_6 = 52
X_7 = 37
X_8 = 22

pixel_to_xy_converter = connect_and_calibrate()
test_main_loop_move_robot(X_END_CHARGE, Y_END_CHARGE)
test_main_loop_move_robot(X_END_CHARGE, Y_END_CHARGE)

# test_main_loop_move_robot(X_END_QR, Y_END_QR)
# test_main_loop_move_robot(X_END_PICKUP, Y_END_PICKUP)
# test_main_loop_move_robot(X_END_DEPOT, Y_END_DEPOT)
# test_main_loop_move_robot(X_END_START, Y_END_START)

# test_main_loop_move_robot(274, 119)

# test_main_loop_move_robot(X_END_TEST, Y_END_TEST)

# test_main_loop_move_robot(X_1, Y_POINT)
# test_main_loop_move_robot(X_2, Y_POINT)
# test_main_loop_move_robot(X_3, Y_POINT)
# test_main_loop_move_robot(X_4, Y_POINT)
# test_main_loop_move_robot(X_5, Y_POINT)
# test_main_loop_move_robot(X_6, Y_POINT)
# test_main_loop_move_robot(X_7, Y_POINT)
# test_main_loop_move_robot(X_8, Y_POINT)




