import cv2
import traceback
import sys
import time

from domain.pathfinding.Astar import Astar
from domain.pathfinding.PathSmoother import PathSmoother
from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from domain.image_analysis.ImageToGridConverter import *
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector
from domain.image_analysis.opencv_callable.DetectStartZone import detect_start_zone
from domain.image_analysis.opencv_callable.DetectZoneDepWorld import detect_zone_dep_world
from domain.image_analysis.opencv_callable.DetectQR import *
from domain.image_analysis.DetectBlurriness import *
from domain.image_analysis_pathfinding.RobotDetector import *

DEBUG = True
ROBOT_DANCE_X_POSITIVE = "50,0,0\n"
ROBOT_DANCE_X_NEGATIVE = "-50,0,0\n"

STRAT_1_Y_CODE_QR = 145
STRAT_2_Y_CODE_QR = 145
STRAT_3_Y_CODE_QR = 145


class Sequence:
    def __init__(self, cap, comm_pi, pixel_to_xy_converter):
        self.cap = cap
        self.X_END = None
        self.Y_END = None
        self.comm_pi = comm_pi
        self.pixel_to_xy_converter = pixel_to_xy_converter
        self.real_path = None
        self.starting_point = None
        self.smooth_path = None
        self.img = None
        self.piece_color = None
        self.depot_number = None
        self.piece_shape = None

    def __create_smooth_path(self):
        while True:
            try:
                self.smooth_path = self.__get_smooth_path()
                break
            except Exception as ex:
                print(ex)
                traceback.print_exc(file=sys.stdout)

    def __get_smooth_path(self):
        center_and_image = None
        while True:
            try:
                center_and_image = self.__find_current_center_robot()
                break
            except Exception as ex:
                print(ex)
                traceback.print_exc(file=sys.stdout)

        grid_converter = ImageToGridConverter(
            center_and_image['image'], center_and_image['center'][0],
            center_and_image['center'][1], self.X_END, self.Y_END)

        astar = Astar(grid_converter.grid, HEIGHT, LENGTH)
        path = astar.find_path()

        path_smoother = PathSmoother(path)
        smooth_path = path_smoother.smooth_path()

        self.__draw_path(smooth_path, grid_converter)

        return smooth_path

    def __convert_to_xy(self):
        self.real_path = self.pixel_to_xy_converter.convert_to_xy(
            self.smooth_path)
        self.starting_point = self.real_path[0]
        self.real_path = self.real_path[1:]

    def __send_coordinates(self):
        for point in self.real_path:
            self.__send_rotation_angle(self.smooth_path)
            x_coord = int(round(point[0] - self.starting_point[0], 0))
            y_coord = int(round(point[1] - self.starting_point[1], 0))
            print("Sending coordinates: " + str(x_coord) + "," + str(y_coord) +
                  ",0")
            self.comm_pi.sendCoordinates(
                str(x_coord) + "," + str(y_coord) + ",0" + "\n")

            while True:
                try:
                    center_and_image = self.__find_current_center_robot()
                    self.starting_point = self.pixel_to_xy_converter.convert_to_xy_point(
                        (center_and_image['center'][0],
                         center_and_image['center'][1]))
                    break
                except Exception as ex:
                    print(ex)
                    traceback.print_exc(file=sys.stdout)

    def __find_current_center_robot(self):
        img = self.take_image_and_draw(self.smooth_path)
        robot_detector = RobotDetector(img)
        return {'center': robot_detector.find_center_of_robot(), 'image': img}

    def __send_rotation_angle(self, path=None):
        while True:
            try:
                img = self.take_image_and_draw(path)
                robot_detector = RobotDetector(img)
                robot_angle = robot_detector.find_angle_of_robot()
                turning_angle = int(round(robot_angle))

                print("Sending angle: " + "0,0," + str(turning_angle) + "\n")
                self.comm_pi.sendCoordinates("0,0," + str(turning_angle) +
                                             "\n")

                break
            except Exception as ex:
                print(ex)
                traceback.print_exc(file=sys.stdout)

    def __draw_path(self, smooth_path, grid_converter):
        for point in smooth_path:
            cv2.circle(grid_converter.image, (point[0], point[1]), 1,
                       [0, 0, 255])

        cv2.imshow("path", grid_converter.image)
        cv2.waitKey(0)

    def take_image_and_draw(self, smooth_path=None):
        print("Capture d'image en cours...")
        ret, img = self.cap.read()

        # cap.release()

        if (smooth_path is not None):
            for point in smooth_path:
                cv2.circle(img, (point[0] * 2, point[1] * 2), 1, [0, 0, 255])

        # cv2.imshow("imageCourante", img)
        # cv2.waitKey()

        cv2.destroyAllWindows()

        return img

    def take_image(self):
        print("Capture d'image en cours...")
        ret, self.img = self.cap.read()

        # cv2.destroyAllWindows()

        return self.img

    def set_end_point(self, x, y):
        self.X_END = x
        self.Y_END = y

    def start(self):
        print("## Starting path finding")
        self.__create_smooth_path()

        print("## Rotating robot")
        self.__send_rotation_angle()

        print("## Convert to X Y")
        self.__convert_to_xy()

        print("## Send coordinates")
        self.__send_coordinates()

    def go_to_start_zone(self):
        img = self.take_image()

        shape = detect_start_zone(img)

        cv2.imshow('ZoneDep', shape.frame)
        cv2.waitKey()

        x, y = shape.center
        self.X_END = round(x / 2)
        self.Y_END = round(y / 2)

    def go_to_zone_dep(self):
        img = self.take_image()
        shape = detect_zone_dep_world(img)
        print(shape)
        x, y = shape.center

        cv2.circle(img, (x, y), 1, [0, 0, 255])

        cv2.imshow("imageCourante", img)
        cv2.waitKey()

        self.X_END = round(x / 2)
        self.Y_END = round(y / 2)

    def end(self):
        self.comm_pi.disconnectFromPi()

    def go_to_qr(self):
        img = self.take_image()
        # x_start, x_end = DetectObstacles(img, STRAT_1_Y_CODE_QR)
        x_start, x_end = 0, 320 - 40
        self.set_end_point(x_end, STRAT_1_Y_CODE_QR)
        self.start()
        self.__dance_to_code_qr(x_start, x_end, STRAT_1_Y_CODE_QR)

    def __dance_to_code_qr(self, x_start, x_end, y_axis):
        x_dance_dist = x_end - x_start
        if (x_dance_dist > 80):
            x_dance_dist = 80

        it = round(x_dance_dist / 20)
        for i in range(it):
            while True:
                img = self.comm_pi.getImage()
                if detect_blurriness(img) is False:
                    break

            if DEBUG:
                cv2.imshow("qr", img)
                cv2.waitKey(0)

            # try to decode qr
            try:
                string = decode(img)
                # FAIRE UN PARSER QUI PARSE ÇA
                self.piece_color = "red"
                self.piece_shape = "square"
                self.depot_number = 1
                print(string)
                if string is not None:
                    break
            except Exception as ex:
                print(ex)

            if (i + 1 == it):
                x_coord = round(x_dance_dist % it) * (i + 1)
                self.set_end_point(x_end - x_coord, y_axis)
                self.start()
            else:
                x_coord = round(x_dance_dist / it) * (i + 1)
                self.set_end_point(x_end - x_coord, y_axis)
                self.start()

    def strats_dance_code_qr(self, strat_number):
        if strat_number == 1:
            self.__dance_to_code_qr(True, 6)
        elif strat_number == 2:
            self.__dance_to_code_qr(True, 5)
        elif strat_number == 3:
            self.__dance_to_code_qr(False, 5)
        elif strat_number == 4:
            self.__dance_to_code_qr(True, 4)
        elif strat_number == 5:
            self.__dance_to_code_qr(False, 4)
        else:
            raise Exception(
                "The number of the strategy for dancing around code qr does not exists"
            )

    def get_tension(self):
        self.comm_pi.getTension()

    def __get_image(self):
        img = None
        while True:
            img = self.comm_pi.getImage()
            if detect_blurriness(img) is False:
                break

        return img

    def go_to_c_charge_station(self):
        self.__send_rotation_angle()
        print("Sending coordinates: -340,-381,0\n")
        time.sleep(0.5)
        self.comm_pi.sendCoordinates("-340,-381,0\n")
        # WAIT TO CHARGE
        time.sleep(1)
        # GET RESPONSE

    def charge_dat_boy_at_charge_station(self):
        while True:
            coord = "0,-2,0\n"
            print("Sending coordinates: " + coord)
            self.comm_pi.sendCoordinates(coord) #move two milimeters in -y to get closer to charge station
            tension = self.comm_pi.getTension()

            time.sleep(3.5) #sleep because it takes 3 seconds for charge station to deliver current

            if tension > 0:
                break

    def go_back_from_charge_station(self):
        print("Sending coordinates: 340,381,0\n")
        time.sleep(0.5)
        self.comm_pi.sendCoordinates("340,381,0\n")
        time.sleep(1)
