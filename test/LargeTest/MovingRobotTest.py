import time
from domain.pathfinding.Astar import Astar
from domain.pathfinding.PathSmoother import PathSmoother
from domain.image_path_analysis.PixelToXYCoordinatesConverter import *
from domain.image_path_analysis.ImageToGridConverter import *
from infrastructure.communication_pi import comm_pi
from domain.image_path_analysis.RobotDetector import RobotDetector

X_END = 75
Y_END = 118
cap = cv2.VideoCapture(0)

def test_main_loop_move_robot():
    #connect to pi
    print("Now connecting...")
    comm_pi.connectToPi()
    time.sleep(5)

    #calibration phase
    print("Calibration phase: ")
    ok = True

    while ok:
        img = take_image()
        print("before pixel to shit")
        pixel_to_xy_converter = PixelToXYCoordinatesConverter(img, CHESS_SQUARE_WIDTH, NUMBER_OF_LINES, NUMBER_OF_COLUMNS)

        ok = False
        break


    #moving robot phase
    print("Starting path finding")
    start = time.time()

    ok = True

    while ok:
        try:
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

            end = time.time()

            print("Found path in: " + str(end - start))

            cv2.imshow("path", grid_converter.image)
            cv2.waitKey(0)

            ok = False
        except Exception as ex:
            print(ex)

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
            time.sleep(10)

            ok = False
        except Exception as ex:
            print(ex)

    real_path = pixel_to_xy_converter.convert_to_xy(smooth_path)
    starting_point = real_path[0]
    real_path = real_path[1:]

    #send coords here
    for point in real_path:
        ok = True

        while ok:
            try:
                img = take_image()

                robot_detector = RobotDetector(img)
                robot_angle = robot_detector.find_angle_of_robot()
                turning_angle = int(round(robot_angle))

                print("Sending angle: " + "0,0," + str(turning_angle) + "\n")
                
                comm_pi.sendCoordinates("0,0," + str(turning_angle) + "\n")
                time.sleep(2)

                ok = False
            except Exception as ex:
                print(ex)

        x_coord = int(round(point[0] - starting_point[0], 0))
        y_coord = int(round(point[1] - starting_point[1], 0))

        print("Sending coordinates: " + str(x_coord) + "," + str(y_coord) + ",0")

        comm_pi.sendCoordinates(str(x_coord) + "," + str(y_coord) + ",0" + "\n")
        time.sleep(2)

        ok = True

        while ok:
            try:
                img = take_image()
                robot_detector = RobotDetector(img)
                x_new, y_new = robot_detector.find_center_of_robot()
                temp = [(x_new, y_new)]
                xy_temp = pixel_to_xy_converter.convert_to_xy(temp)
                starting_point = xy_temp[0]

                ok = False
            except Exception as ex:
                print(ex)


def take_image():
    print("Capture d'image en cours...")
    ret, img = cap.read()
    #cap.release()

    # cv2.imshow("imageCourante", img)
    #cv2.waitKey()

    cv2.destroyAllWindows()

    return img


test_main_loop_move_robot()
