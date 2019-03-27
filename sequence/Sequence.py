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
from domain.image_analysis.opencv_callable.DetectPickupZone import detect_pickup_zone
from domain.image_analysis.opencv_callable.DetectQR import *
from domain.image_analysis.DetectBlurriness import *
from domain.image_analysis_pathfinding.RobotDetector import *
from domain.pathfinding.Exceptions.NoPathFoundException import *
from domain.pathfinding.Exceptions.NoBeginingPointException import *
from domain.image_analysis.opencv_callable.DetectPiece import *
from domain.QRCodeDictionnary import *
from util.Logger import Logger
from domain.image_analysis.Cardinal import *

DEBUG = True
ROBOT_DANCE_X_POSITIVE = "50,0,0\n"
ROBOT_DANCE_X_NEGATIVE = "-50,0,0\n"

STRAT_1_Y_CODE_QR = 145
STRAT_2_Y_CODE_QR = 145
STRAT_3_Y_CODE_QR = 145

X_END_START_ZONE = 81
Y_END_START_ZONE = 121

Y_ARRAY_FOR_QR_STRATEGY = [120, 145, 170, 90]

X_RANGE_FOR_QR_STRATEGY = [200, 230, 260, 285]

OFFSET_Y_CAM_EMBARKED = 80
OFFSET_X_CAM_EMBARKED = -23

logger = Logger(__name__)


class Sequence:
    def __init__(self, cap, comm_pi, world_cam_pixel_to_xy_converter,
                 robot_cam_pixel_to_xy_converter):
        self.cap = cap
        self.X_END = None
        self.Y_END = None
        self.comm_pi = comm_pi
        self.world_cam_pixel_to_xy_converter = world_cam_pixel_to_xy_converter
        self.robot_cam_pixel_to_xy_converter = robot_cam_pixel_to_xy_converter
        self.real_path = None
        self.starting_point = None
        self.smooth_path = None
        self.img = None
        self.piece_color = None
        self.depot_number = None
        self.piece_shape = None
        self.retry = 0
        self.zone_dep_cardinal = None
        self.zone_dep_point = None
        self.zone_pickup_cardinal = None
        self.zone_pickup_point = None
        self.zone_start_point = None
        self.__init_zones()

    def __init_zones(self):
        self.__detect_start_zone()
        self.__detect_zone_dep()
        self.__detect_pickup_zone()

        img = self.take_image()

        cv2.circle(img, ((self.zone_dep_point[0] * 2),
                         (self.zone_dep_point[1] * 2)), 1, [0, 0, 255])
        cv2.circle(img, ((self.zone_pickup_point[0] * 2),
                         (self.zone_pickup_point[1] * 2)), 1, [0, 0, 255])
        cv2.circle(img, ((self.zone_start_point[0] * 2),
                         (self.zone_start_point[1] * 2)), 1, [0, 0, 255])

        cv2.imshow("ZONES FOUND", img)
        cv2.waitKey(0)

    def __detect_start_zone(self):

        i = 0
        while True:
            try:
                img = self.take_image()
                i = i + 1
                (x, y) = detect_start_zone(img)
                if (i > 20):
                    logger.log_critical(
                        'START ZONE NOT DETECTED, FALL BACK TO HARDCODED')
                    logger.log_debug(traceback.format_exc())
                    self.zone_start_point = (X_END_START_ZONE,
                                             Y_END_START_ZONE)
                    break

                self.zone_start_point = (round(x / 2), round(y / 2))
                break
            except Exception:
                logger.log_debug('START ZONE NOT DETECTED RETRYING' + str(i))

    def __detect_zone_dep(self):

        i = 0
        while True:
            try:
                img = self.take_image()
                i = i + 1
                res = detect_zone_dep_world(img)
                (x, y) = res['point']
                self.zone_dep_point = (round(x / 2), round(y / 2))
                self.zone_dep_cardinal = res['cardinal']
                break
            except Exception:
                logger.log_debug('ZONE DEP WORLD NOT DETECTED RETRYING' +
                                 str(i))
                if (i > 20):
                    logger.log_critical(
                        'ZONE DEP WORLD NOT DETECTED PROBLEMS, PROBLEMS, PROBLEMS'
                    )
                    logger.log_debug(traceback.format_exc())
                    raise Exception(
                        'ZONE DEP WORLD NOT DETECTED PROBLEMS, PROBLEMS, PROBLEMS'
                    )

    def __detect_pickup_zone(self):

        i = 0
        while True:
            try:
                img = self.take_image()
                i = i + 1
                res = detect_pickup_zone(img)
                (x, y) = res['point']
                self.zone_pickup_point = (round(x / 2), round(y / 2))
                self.zone_pickup_cardinal = res['cardinal']
                break
            except Exception:
                logger.log_debug('PICKUP ZONE NOT DETECTED RETRYING' + str(i))
                if (i > 20):
                    logger.log_critical(
                        'PICKUP ZONE NOT DETECTED PROBLEMS, PROBLEMS, PROBLEMS'
                    )
                    logger.log_debug(traceback.format_exc())
                    raise Exception(
                        'PICKUP ZONE NOT DETECTED PROBLEMS, PROBLEMS, PROBLEMS'
                    )

    def __create_smooth_path(self, unsecure=False):
        center_and_image = None
        while True:
            try:
                center_and_image = self.__find_current_center_robot()
                break
            except Exception as ex:
                logger.log_error(ex)
                logger.log_critical(traceback.format_exc())

        grid_converter = None
        try:
            if unsecure:
                self.retry = self.retry + 1
                print(self.retry)
                print(OBSTACLE_BORDER - 5 * self.retry)
                grid_converter = ImageToGridConverter(
                    center_and_image['image'], center_and_image['center'][0],
                    center_and_image['center'][1], self.X_END, self.Y_END,
                    OBSTACLE_BORDER - 5 * self.retry,
                    LEFT_OBSTACLE_BORDER - 5 * self.retry)
                logger.log_critical(
                    "Unsecure pathfinding with new grid converter with new value for obstacle border: "
                    + str(grid_converter.get_obstacle_border()))
            else:
                grid_converter = ImageToGridConverter(
                    center_and_image['image'], center_and_image['center'][0],
                    center_and_image['center'][1], self.X_END, self.Y_END)

            astar = Astar(grid_converter.grid, HEIGHT, LENGTH)
            path = astar.find_path()

            path_smoother = PathSmoother(path)
            smooth_path = path_smoother.smooth_path()
            self.__draw_path(smooth_path, grid_converter)

            self.smooth_path = smooth_path
        except Exception as ex:
            if (isinstance(ex, NoBeginingPointException)):
                logger.log_debug('NoBeginingPointException have been raised')
                logger.log_debug(ex)
                logger.log_debug(traceback.format_exc())
                self.__create_smooth_path(True)
                pass
            else:
                logger.log_debug(ex)
                logger.log_debug(traceback.format_exc())
                if (DEBUG):
                    frame = self.take_image()
                    cv2.circle(frame, (self.X_END * 2, self.Y_END * 2), 1,
                               [0, 0, 255])
                    cv2.imshow('OBSTACLE PATH', frame)
                    cv2.waitKey()
                raise ex

    def __convert_to_xy(self):
        self.real_path = self.world_cam_pixel_to_xy_converter.convert_to_xy(
            self.smooth_path)
        self.starting_point = self.real_path[0]
        self.real_path = self.real_path[1:]

    def __send_coordinates(self):
        for point in self.real_path:
            self.__send_rotation_angle(self.smooth_path)
            x_coord = int(round(point[0] - self.starting_point[0], 0))
            y_coord = int(round(point[1] - self.starting_point[1], 0))
            self.comm_pi.sendCoordinates(
                str(x_coord) + "," + str(y_coord) + ",0" + "\n")

            while True:
                try:
                    center_and_image = self.__find_current_center_robot()
                    self.starting_point = self.world_cam_pixel_to_xy_converter.convert_to_xy_point(
                        (center_and_image['center'][0],
                         center_and_image['center'][1]))
                    break
                except Exception as ex:
                    logger.log_error(ex)
                    logger.log_critical(traceback.format_exc())

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
                self.comm_pi.sendAngle(turning_angle)
                break
            except Exception as ex:
                logger.log_error(ex)
                logger.log_debug(traceback.format_exc())

    def __draw_path(self, smooth_path, grid_converter):
        for point in smooth_path:
            cv2.circle(grid_converter.image, (point[0], point[1]), 1,
                       [0, 0, 255])

        cv2.imshow("path", grid_converter.image)
        cv2.waitKey(0)

    def take_image_and_draw(self, smooth_path=None):
        logger.log_info("Capture d'image en cours...")
        ret, img = self.cap.read()

        # cap.release()

        if (smooth_path is not None):
            for point in smooth_path:
                cv2.circle(img, (point[0] * 2, point[1] * 2), 1, [0, 0, 255])

        if (DEBUG):
            cv2.imshow("imageCourante", img)
            cv2.waitKey()

        cv2.destroyAllWindows()

        return img

    def take_image(self):
        logger.log_info("Capture d'image en cours...")
        ret, self.img = self.cap.read()

        # cv2.destroyAllWindows()

        return self.img

    def set_end_point(self, x, y):
        self.X_END = x
        self.Y_END = y

    def start(self):
        logger.log_info("## Starting path finding")
        self.__create_smooth_path()

        logger.log_info("## Rotating robot")
        self.__send_rotation_angle()

        logger.log_info("## Convert to X Y")
        self.__convert_to_xy()

        logger.log_info("## Send coordinates")
        self.__send_coordinates()

    def go_to_start_zone(self):
        self.set_end_point(self.zone_start_point[0], self.zone_start_point[1])
        self.start()

    def go_to_zone_dep(self):
        self.set_end_point(self.zone_dep_point[0], self.zone_dep_point[1])
        self.start()

    def go_to_zone_pickup(self):
        self.comm_pi.changeServoHori('2000')
        self.set_end_point(self.zone_pickup_point[0],
                           self.zone_pickup_point[1])
        self.start()

    def end(self):
        self.comm_pi.disconnectFromPi()

    def go_to_decode_qr(self):
        self.comm_pi.changeServoVert('6000')
        self.comm_pi.changeServoHori('5500')
        stop_outer_loop = False
        for y in Y_ARRAY_FOR_QR_STRATEGY:
            for x in X_RANGE_FOR_QR_STRATEGY:
                self.set_end_point(x, y)
                try:
                    self.start()
                    stop_outer_loop = self.__try_to_decode_qr()
                    if (stop_outer_loop):
                        break
                except Exception as ex:
                    logger.log_error(ex)
                    logger.log_debug(
                        'Decode QR fallback to other point, obstacle in the way'
                    )
                    logger.log_debug(traceback.format_exc())
                    pass

            if stop_outer_loop:
                break

    def __try_to_decode_qr(self):
        img = None
        while True:
            img = self.comm_pi.getImage()
            if detect_blurriness(img) is False:
                break

        if DEBUG:
            cv2.imshow("qr", img)
            cv2.waitKey(0)

        # try to decode qr
        dict_of_values = decode(img)
        self.piece_color = dict_of_values[COULEUR]
        self.piece_shape = dict_of_values[PIECE]
        self.depot_number = dict_of_values[ZONE]
        logger.log_info("Values of qr code: " + str(dict_of_values))

        if dict_of_values is None:
            return False

        return True
        # assign attributes for further uses

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
        time.sleep(0.5)
        self.comm_pi.sendCoordinates("-340,-381,0\n")
        # WAIT TO CHARGE
        time.sleep(1)
        # GET RESPONSE

    def charge_robot_at_station(self):
        increment = 0
        while True:
            coord = "0,-7,0\n"
            self.comm_pi.sendCoordinates(
                coord
            )  # move two milimeters in -y to get closer to charge station
            time.sleep(
                3.5
            )  # sleep because it takes 3 seconds for charge station to deliver current
            tension = self.comm_pi.getTension()

            if tension > 0 or increment == 5:
                break

            increment += 1

        logger.log_info("Charging robot waiting for that electric feel now...")
        time.sleep(10)  # code here to wait for robot to be charged
        logger.log_info("Robot is charged now!")

    def go_back_from_charge_station(self):
        time.sleep(0.5)
        self.comm_pi.sendCoordinates("340,381,0\n")
        time.sleep(1)

    def move_robot_around_pickup_zone(self):
        x_mm_movement_point = (30, 0)
        x_mm_movement_point_negative = (-30, 0)
        y_mm_movement_point = (0, 30)
        y_mm_movement_point_negative = (0, -30)
        number_of_increment = 8

        if self.zone_pickup_cardinal == SOUTH():
            logger.log_info("Move around south pick up...")
            for i in range(number_of_increment):
                x, y = self.robot_cam_pixel_to_xy_converter.convert_real_xy_given_angle(
                    x_mm_movement_point_negative, -90)
                self.comm_pi.sendCoordinates(str(x) + "," + str(y) + ",0\n")
                piece_grabbed = self.grab_piece()

                if piece_grabbed:
                    break

        if self.zone_pickup_cardinal == NORTH():
            logger.log_info("Move around north pick up...")
            for i in range(number_of_increment):
                x, y = self.robot_cam_pixel_to_xy_converter.convert_real_xy_given_angle(
                    x_mm_movement_point, 90)
                self.comm_pi.sendCoordinates(str(x) + "," + str(y) + ",0\n")

                piece_grabbed = self.grab_piece()

                if piece_grabbed:
                    break

        if self.zone_pickup_cardinal == EAST():
            logger.log_info("Move around east pick up...")
            for i in range(number_of_increment):
                x, y = self.robot_cam_pixel_to_xy_converter.convert_real_xy_given_angle(
                    y_mm_movement_point_negative, 0)
                self.comm_pi.sendCoordinates(str(x) + "," + str(y) + ",0\n")

                piece_grabbed = self.grab_piece()

                if piece_grabbed:
                    break

        if self.zone_pickup_cardinal == WEST():
            logger.log_info("Move around west pick up...")
            for i in range(number_of_increment):
                x, y = self.robot_cam_pixel_to_xy_converter.convert_real_xy_given_angle(
                    y_mm_movement_point, 180)
                self.comm_pi.sendCoordinates(str(x) + "," + str(y) + ",0\n")

                piece_grabbed = self.grab_piece()

                if piece_grabbed:
                    break

    def grab_piece(self):
        logger.log_info("Trying to grab piece...")
        robot_img = self.comm_pi.getImage()
        height, width, channels = robot_img.shape

        try:
            x, y = detect_piece(robot_img, self.piece_shape, self.piece_color)
            logger.log_info("Found piece!")
        except Exception as ex:
            logger.log_critical(
                "Could not find piece, continuing to move to detect it...")
            logger.log_critical(traceback.print_exc())
            return False

        x_from_center_of_image = round(x - (
            (width / 2) + OFFSET_X_CAM_EMBARKED))
        y_from_center_of_image = round(y - (
            (height / 2) + OFFSET_Y_CAM_EMBARKED))

        real_x, real_y = self.robot_cam_pixel_to_xy_converter\
            .convert_pixel_to_xy_point_given_angle((x_from_center_of_image, y_from_center_of_image),
                                                   self.__cardinal_to_angle(self.zone_pickup_cardinal))

        if DEBUG:
            robot_img = self.take_image()
            cv2.circle(robot_img, (x, y), 5, [255, 255, 255])
            cv2.circle(robot_img,
                       (x_from_center_of_image, y_from_center_of_image), 5,
                       [255, 255, 255])
            cv2.imshow("grab piece frame", robot_img)
            logger.log_info("Real moving point: " + str(real_x) + "," +
                            str(real_y))

        string_coord = str(real_x) + "," + str(real_y) + ",0\n"
        self.comm_pi.sendCoordinates(string_coord)

        # activate arm here
        # here return true of false to know if piece was really grabbed

        return True

    def __cardinal_to_angle(self, cardinal_str):

        if cardinal_str == EAST():
            return 0
        elif cardinal_str == NORTH():
            return 90
        elif cardinal_str == WEST():
            return 180
        elif cardinal_str == SOUTH():
            return -90
        else:
            return None

    def rotate_robot_on_zone_dep(self):
        logger.log_info("Rotate on sone dep plane...")
        self.__rotate_robot_on_zone_plane(self.zone_dep_cardinal)

    def rotate_robot_on_zone_pickup(self):
        logger.log_info("Rotate on pickup zone plane...")
        self.__rotate_robot_on_zone_plane(self.zone_pickup_cardinal)

    def __rotate_robot_on_zone_plane(self, cardinal_point, first_it=True):
        img = self.take_image()
        robot_detector = RobotDetector(img)
        robot_angle = robot_detector.find_angle_of_robot()

        if cardinal_point == EAST():
            logger.log_info("Rotate to east...")
            self.__rotate_to_east(robot_angle)
            if first_it:
                self.__rotate_robot_on_zone_plane(EAST(), False)

        if cardinal_point == SOUTH():
            logger.log_info("Rotate to south...")
            self.__rotate_to_south(robot_angle)
            if first_it:
                self.__rotate_robot_on_zone_plane(SOUTH(), False)

        if cardinal_point == WEST():
            logger.log_info("Rotate to west...")
            self.__rotate_to_west(robot_angle)
            if first_it:
                self.__rotate_robot_on_zone_plane(WEST(), False)

        if cardinal_point == NORTH():
            logger.log_info("Rotate to north...")
            self.__rotate_to_north(robot_angle)
            if first_it:
                self.__rotate_robot_on_zone_plane(NORTH(), False)

    def __rotate_to_north(self, current_robot_angle):
        rotate_angle = round(90 - current_robot_angle) * -1
        self.comm_pi.sendAngle(rotate_angle)

    def __rotate_to_east(self, current_robot_angle):
        rotate_angle = round(0 - current_robot_angle) * -1
        self.comm_pi.sendAngle(rotate_angle)

    def __rotate_to_south(self, current_robot_angle):
        rotate_angle = round(-90 - current_robot_angle) * -1
        self.comm_pi.sendAngle(rotate_angle)

    def __rotate_to_west(self, current_robot_angle):
        rotate_angle = round(180 - current_robot_angle) * -1
        self.comm_pi.sendAngle(rotate_angle)
