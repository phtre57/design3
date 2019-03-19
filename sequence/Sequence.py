import cv2
import traceback

from domain.pathfinding.Astar import Astar
from domain.pathfinding.PathSmoother import PathSmoother
from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from domain.image_analysis.ImageToGridConverter import *
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector

class Sequence:
    def __init__(self, cap, X_END, Y_END, comm_pi, pixel_to_xy_converter):
        self.cap = cap
        self.X_END = X_END
        self.Y_END = Y_END
        self.comm_pi = comm_pi
        self.pixel_to_xy_converter = pixel_to_xy_converter
        self.real_path = None
        self.starting_point = None
        self.smooth_path = None

    def create_smooth_path(self):
        while True:
            try:
                self.smooth_path = self.__get_smooth_path()            
                break
            except Exception as ex:
                print(ex)
                traceback.print_exc(file=sys.stdout)

    def __get_smooth_path(self):
        resp = self.__find_current_center_robot()
        grid_converter = ImageToGridConverter(resp['image'], resp['center'][0], resp['center'][1], self.X_END, self.Y_END)

        astar = Astar(grid_converter.grid, HEIGHT, LENGTH)
        path = astar.find_path()

        path_smoother = PathSmoother(path)
        smooth_path = path_smoother.smooth_path()

        self.__draw_path(smooth_path, grid_converter)

        return smooth_path

    def convert_to_xy(self):
        self.real_path = self.pixel_to_xy_converter.convert_to_xy(self.smooth_path)
        print(self.real_path)
        self.starting_point = self.real_path[0]
        self.real_path = self.real_path[1:]

    def send_coordinates(self):
        for point in self.real_path:
            self.get_rotation_angle(self.smooth_path)
            x_coord = int(round(point[0] - self.starting_point[0], 0))
            y_coord = int(round(point[1] - self.starting_point[1], 0))
            print("Sending coordinates: " + str(x_coord) + "," + str(y_coord) + ",0")
            self.comm_pi.sendCoordinates(str(x_coord) + "," + str(y_coord) + ",0" + "\n")

            while True:
                try:
                    resp = self.__find_current_center_robot()
                    self.starting_point = self.pixel_to_xy_converter.convert_to_xy_point((resp['center'][0], resp['center'][1]))
                    break
                except Exception as ex:
                    print(ex)
                    traceback.print_exc(file=sys.stdout)

    def __find_current_center_robot(self):
        img = self.take_image(self.smooth_path)
        robot_detector = RobotDetector(img)
        return { 'center': robot_detector.find_center_of_robot(), 'image': img }
    
    def get_rotation_angle(self, smooth_path = None):
        while True:
            try:
                img = self.take_image(smooth_path)
                robot_detector = RobotDetector(img)
                robot_angle = robot_detector.find_angle_of_robot()
                turning_angle = int(round(robot_angle))

                print("Sending angle: " + "0,0," + str(turning_angle) + "\n")
                self.comm_pi.sendCoordinates("0,0," + str(turning_angle) + "\n")

                break
            except Exception as ex:
                print(ex)
                traceback.print_exc(file=sys.stdout)

    def __draw_path(self, smooth_path, grid_converter):
        for point in smooth_path:
            cv2.circle(grid_converter.image, (point[0], point[1]), 1, [0, 0, 255])

        cv2.imshow("path", grid_converter.image)
        cv2.waitKey(0)

    def take_image(self, smooth_path = None):
        print("Capture d'image en cours...")
        ret, img = self.cap.read()

        #cap.release()

        if (smooth_path is not None):
            for point in smooth_path:
                cv2.circle(img, (point[0]*2, point[1]*2), 1, [0, 0, 255])

        # cv2.imshow("imageCourante", img)
        # cv2.waitKey()

        cv2.destroyAllWindows()

        return img