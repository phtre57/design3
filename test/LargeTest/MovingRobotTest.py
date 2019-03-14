import time
from domain.pathfinding.Astar import Astar
from domain.pathfinding.PathSmoother import PathSmoother
from domain.image_path_analysis.PixelToXYCoordinatesConverter import *
from domain.image_path_analysis.ImageToGridConverter import *
from infrastructure.communication_pi import comm_pi
from domain.image_path_analysis.RobotDetector import RobotDetector


def test_main_loop_move_robot():
    #connect to pi
    print("Now connecting...")
    #comm_pi.connectToPi()
    #time.sleep(5)

    #calibration phase
    print("Calibration phase: ")
    ok = True

    while ok:
        try:
            img = take_image()

            pixel_to_xy_converter = PixelToXYCoordinatesConverter(img, CHESS_SQUARE_WIDTH)

            ok = False
        except Exception as ex:
            print(ex)

    #Rotating robot to 0 degree
    print("Rotating robot phase: ")
    ok = True

    while ok:
        try:
            img = take_image()

            robot_detector = RobotDetector(img)
            robot_angle = robot_detector.find_angle_of_robot()

            #here send negative the angle found to robot...
            ok = False
        except Exception as ex:
            print(ex)

    #moving robot phase
    print("Starting path finding")
    start = time.time()

    ok = True

    while ok:
        try:
            img = take_image()

            robot_detector = RobotDetector(img)
            x_start, y_start = robot_detector.find_center_of_robot()

            grid_converter = ImageToGridConverter(img, x_start, y_start, 50, 50)

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

    real_path = pixel_to_xy_converter.convert_to_xy(smooth_path)
    starting_point = real_path[0]
    real_path = real_path[1:]

    #send coords here
    for point in real_path:
        x_coord = round(point[0] - starting_point[0])
        y_coord = round(point[1] - starting_point[1])

        print("Sending coordinates: (" + x_coord + ", " + y_coord + ")")

        #comm_pi.sendCoordinates(str(x_coord) + "," + str(y_coord) + "\n")
        #time.sleep(5)

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
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    cap.release()

    cv2.imshow(img, "imageCourante")
    cv2.waitKey(0)

    return img


test_main_loop_move_robot()
