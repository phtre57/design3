import time
from domain.pathfinding.Astar import Astar
from domain.pathfinding.PathSmoother import PathSmoother
from domain.image_path_analysis.PixelToXYCoordinatesConverter import *
from domain.image_path_analysis.ImageToGridConverter import *
from infrastructure.communication_pi import comm_pi
from domain.image_path_analysis.RobotDetector import RobotDetector

#this test do not reassess position of robot
def test_main_loop_move_robot():
    #connect to pi
    print("Now connecting...")
    comm_pi.connectToPi()
    time.sleep(5)

    #calibration phase
    print("Calibration phase: ")
    img = take_image()

    pixel_to_xy_converter = PixelToXYCoordinatesConverter(img, CHESS_SQUARE_WIDTH)

    #moving robot phase
    print("Starting path finding")
    img = take_image()

    start = time.time()

    robot_detector = RobotDetector(img)
    x_start, y_start = robot_detector.find_center_of_robot()

    grid_converter = ImageToGridConverter(img, x_start, y_start, 50, 50)

    astar = Astar(grid_converter.grid, HEIGHT, LENGTH)

    path = astar.find_path()

    path_smoother = PathSmoother(path)
    smooth_path = path_smoother.smooth_path()

    end = time.time()

    print("Found path in: " + str(end - start))

    real_path = pixel_to_xy_converter.convert_to_xy(smooth_path)
    starting_point = real_path[0]
    real_path = real_path[1:]

    #send coords here
    for point in real_path:
        x_coord = round(point[0] - starting_point[0])
        y_coord = round(point[1] - starting_point[1])

        print("Sending coordinates: (" + x_coord + ", " + y_coord + ")")

        comm_pi.sendCoordinates(str(x_coord) + "," + str(y_coord) + "\n")
        time.sleep(5)

        starting_point = point


def take_image():
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    cap.release()

    cv2.imshow(img, "imageCourante")
    cv2.waitKey(0)

    return img


test_main_loop_move_robot()
