import cv2
import traceback
import sys
import time

from domain.pathfinding.Astar import Astar
from domain.pathfinding.PathSmoother import PathSmoother
from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from domain.image_analysis.ImageToGridConverter import *
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector
from domain.image_analysis.opencv_callable.DetectQR import *
from domain.image_analysis.DetectBlurriness import *
from domain.image_analysis_pathfinding.RobotDetector import *
from domain.pathfinding.Exceptions.NoPathFoundException import *
from domain.pathfinding.Exceptions.NoBeginingPointException import *
from domain.image_analysis.opencv_callable.DetectPiece import *
from domain.QRCodeDictionnary import *
from util.Logger import Logger
from domain.image_analysis.Cardinal import *
from domain.image_analysis.opencv_callable.DetectPointZoneDep import detect_point_zone_dep
from sequence.InitSequence import InitSequence
from domain.RobotMover import *

DEBUG = False
ROBOT_DANCE_X_POSITIVE = "50,0,0\n"
ROBOT_DANCE_X_NEGATIVE = "-50,0,0\n"

STRAT_1_Y_CODE_QR = 145
STRAT_2_Y_CODE_QR = 145
STRAT_3_Y_CODE_QR = 145

X_END_START_ZONE = 81
Y_END_START_ZONE = 121

Y_ARRAY_FOR_QR_STRATEGY = [120, 145, 170, 90]

X_RANGE_FOR_QR_STRATEGY = [200, 230, 260, 285]

NUMBER_OF_INCREMENT_PICKUP_ZONE = 15

TENSION_THRESHOLD = 3.5

logger = Logger(__name__)


class Sequence:
    def __init__(self, image_taker, comm_pi, world_cam_pixel_to_xy_converter,
                 robot_cam_pixel_to_xy_converter):
        self.image_taker = image_taker
        self.X_END = None
        self.Y_END = None
        self.comm_pi = comm_pi
        self.world_cam_pixel_to_xy_converter = world_cam_pixel_to_xy_converter
        self.robot_cam_pixel_to_xy_converter = robot_cam_pixel_to_xy_converter
        self.robot_mover = RobotMover(world_cam_pixel_to_xy_converter,
                                      robot_cam_pixel_to_xy_converter)
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
        self.__init_sequence()
        self.comm_pi.moveArm('2000')

    def __init_sequence(self):
        initSequence = InitSequence(X_END_START_ZONE, Y_END_START_ZONE,
                                    self.image_taker)
        self.zone_start_point, self.zone_dep_cardinal, self.zone_dep_point, self.zone_pickup_cardinal, self.zone_pickup_point = initSequence.init(
        )

        img = self.take_image()

        cv2.circle(img, ((self.zone_dep_point[0] * 2),
                         (self.zone_dep_point[1] * 2)), 1, [0, 0, 255])
        cv2.circle(img, ((self.zone_pickup_point[0] * 2),
                         (self.zone_pickup_point[1] * 2)), 1, [0, 0, 255])
        cv2.circle(img, ((self.zone_start_point[0] * 2),
                         (self.zone_start_point[1] * 2)), 1, [0, 0, 255])

        cv2.imshow("ZONES FOUND", img)
        cv2.waitKey(0)

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
                # grid_converter = ImageToGridConverter(
                #     center_and_image['image'], center_and_image['center'][0],
                #     center_and_image['center'][1], self.X_END, self.Y_END, 0,
                #     0, CIRCLE_OBSTACLE_RADIUS, True)

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
            self.comm_pi.sendCoordinates(x_coord, y_coord)

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
                if (abs(turning_angle) > 3):
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
        ret, img = self.image_taker.read()

        if (smooth_path is not None):
            for point in smooth_path:
                cv2.circle(img, (point[0] * 2, point[1] * 2), 1, [0, 0, 255])

        cv2.destroyAllWindows()

        return img

    def take_image(self):
        logger.log_info("Capture d'image de la camera monde en cours...")

        while True:
            ret, self.img = self.image_taker.read()
            if ret:
                break

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
        self.__rotate_robot_on_zone_dep()

    def go_to_zone_pickup(self):
        self.comm_pi.changeServoVert('6000')
        self.comm_pi.changeServoHori('2000')
        self.set_end_point(self.zone_pickup_point[0],
                           self.zone_pickup_point[1])
        self.start()
        self.__rotate_robot_on_zone_pickup()

    def end(self):
        self.comm_pi.redLightOff()
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
        img = self.__get_image()

        if DEBUG:
            cv2.imshow("qr", img)
            cv2.waitKey(0)

        # try to decode qr
        dict_of_values = decode(img)
        self.piece_color = dict_of_values[COULEUR]
        self.piece_shape = dict_of_values[PIECE]
        self.depot_number = dict_of_values[ZONE]
        logger.log_info("Values of qr code: " + str(dict_of_values))
        logger.log_info(
            ("Value of self.piece_color: " + str(self.piece_color)))
        logger.log_info(
            ("Value of self.piece_shape: " + str(self.piece_shape)))
        logger.log_info(
            ("Value of self.depot_number: " + str(self.depot_number)))

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

    def go_to_charge_robot(self):
        decision_tension = self.__is_current_tension_too_high_to_charge()
        if (decision_tension):
            return

        self.__go_to_c_charge_station()
        self.__charge_robot_at_station()
        self.__go_back_from_charge_station()

    def __is_current_tension_too_high_to_charge(self):
        tension = self.comm_pi.getTension()
        if (tension > TENSION_THRESHOLD):
            return True
        else:
            return False

    def __go_to_c_charge_station(self):
        self.__send_rotation_angle()
        time.sleep(0.5)
        self.comm_pi.sendCoordinates(-360, -381)
        time.sleep(1)

    def __charge_robot_at_station(self):
        self.comm_pi.changeCondensateurHigh()
        base_tension = self.comm_pi.getTension()

        increment = 0
        while True:
            self.comm_pi.sendCoordinates(0, -13)
            time.sleep(1.5)

            derivative_tension = 0
            tension = 0
            for i in range(10):
                time.sleep(0.5)
                tension = self.comm_pi.getTension()

                if tension <= base_tension:
                    derivative_tension = 0

                if tension > base_tension:
                    derivative_tension += 1
                    base_tension = tension

                if derivative_tension > 5:
                    break

            if tension > base_tension:
                break

            increment += 1

        logger.log_info("Charging robot waiting for that electric feel now...")

        while True:
            time.sleep(0.3)
            tension = self.comm_pi.getTension()
            logger.log_info('Tension now while charging ' + str(tension))
            if tension > 4.30:
                break

        logger.log_info("Robot is charged now!")

    def __go_back_from_charge_station(self):
        time.sleep(0.5)
        self.comm_pi.sendCoordinates(360, 381)
        time.sleep(1)

    def move_robot_around_pickup_zone(self):
        self.__try_to_move_robot_around_pickup_zone()
        (x, y) = self.robot_mover.fallback_from_cardinality(
            self.zone_pickup_cardinal)
        self.comm_pi.sendCoordinates(x, y)

    def __try_to_move_robot_around_pickup_zone(self):
        MOVEMENT_OFFSET = 20
        self.comm_pi.changeCondensateurLow()
        x_mm_movement_point = (MOVEMENT_OFFSET, 0)
        x_mm_movement_point_negative = (-1 * MOVEMENT_OFFSET, 0)
        y_mm_movement_point = (0, MOVEMENT_OFFSET)
        y_mm_movement_point_negative = (0, -1 * MOVEMENT_OFFSET)

        if self.zone_pickup_cardinal == SOUTH():
            logger.log_info("Move around south pick up...")
            self.__validate_if_pickup_sequence_is_done_and_move(
                x_mm_movement_point_negative, -90)

        if self.zone_pickup_cardinal == NORTH():
            logger.log_info("Move around north pick up...")
            self.__validate_if_pickup_sequence_is_done_and_move(
                x_mm_movement_point, 90)

        if self.zone_pickup_cardinal == EAST():
            logger.log_info("Move around east pick up...")
            self.__validate_if_pickup_sequence_is_done_and_move(
                y_mm_movement_point_negative, 0)

        if self.zone_pickup_cardinal == WEST():
            logger.log_info("Move around west pick up...")
            self.__validate_if_pickup_sequence_is_done_and_move(
                y_mm_movement_point, 180)

    def __validate_if_pickup_sequence_is_done_and_move(self, movement_point,
                                                       angle):
        piece_grabbed = False
        while not piece_grabbed:
            piece_grabbed, real_x, real_y = self.__move_on_pickup_zone(
                movement_point, angle)

            if piece_grabbed:
                validate_piece_was_grabbed = self.validate_piece_taken(
                    real_x, real_y)
                if validate_piece_was_grabbed is False:
                    self.__try_to_move_robot_around_pickup_zone()

                break

            (x, y) = self.robot_mover.fallback_from_cardinality(
                self.zone_pickup_cardinal)
            self.comm_pi.sendCoordinates(x, y)
            self.go_to_zone_pickup()

    def __move_on_pickup_zone(self, moving_point, angle):
        number_of_increment = NUMBER_OF_INCREMENT_PICKUP_ZONE
        i = 0

        while i < number_of_increment:

            x, y = self.robot_cam_pixel_to_xy_converter.convert_real_xy_given_angle(
                moving_point, angle)
            self.comm_pi.sendCoordinates(x, y)

            piece_grabbed, real_x, real_y = self.grab_piece()

            if piece_grabbed:
                break

            i += 1
        return (piece_grabbed, real_x, real_y)

    def validate_piece_taken(self, x, y):
        self.comm_pi.sendCoordinates(x * -1, y * -1)
        robot_img = self.comm_pi.getImage()

        try:
            x, y = detect_piece(robot_img, self.piece_shape, self.piece_color)
            logger.log_critical("VALIDATE PIECE TAKEN - FOUND ONE...")
            return False
        except Exception:
            logger.log_critical("VALIDATE PIECE TAKEN - Yes we grabbed it...")
            logger.log_critical(traceback.print_exc())
            return True

    def grab_piece(self):
        logger.log_info("Trying to grab piece...")
        robot_img = self.comm_pi.getImage()
        height, width, channels = robot_img.shape

        try:
            x, y = detect_piece(robot_img, self.piece_shape, self.piece_color)
            logger.log_info("Found piece!")
        except Exception:
            logger.log_critical(
                "Could not find piece, continuing to move to detect it...")
            logger.log_critical(traceback.print_exc())
            return False, 0, 0

        real_x, real_y = self.robot_mover.move_robot_from_embarked_referential(
            x, y, self.zone_pickup_cardinal, width, height)
        if DEBUG:
            robot_img = self.take_image()
            cv2.circle(robot_img, (x, y), 5, [255, 255, 255])
            cv2.imshow("grab piece frame", robot_img)
            logger.log_info("Real moving point: " + str(real_x) + "," +
                            str(real_y))

        if real_y < -80:
            logger.log_critical("Piece point is too far : " + str(real_x) +
                                ", " + str(real_y))
            return False, 0, 0

        logger.log_critical("Piece point accepted and sent : " + str(real_x) +
                            ", " + str(real_y))

        self.comm_pi.sendCoordinates(round(real_x), round(real_y))

        logger.log_info('Activate the arm')
        time.sleep(0.5)
        self.comm_pi.moveArm('7800')
        time.sleep(1.5)
        logger.log_info('Lifting the arm')
        self.comm_pi.moveArm('2000')

        # here return true of false to know if piece was really grabbed

        return True, real_x, real_y

    def move_robot_around_zone_dep(self):
        while True:
            try:
                self.__move_to_point_zone_dep()
                self.drop_piece()
                (x, y) = self.robot_mover.fallback_from_cardinality(
                    self.zone_dep_cardinal)
                self.comm_pi.sendCoordinates(x, y)
                break
            except Exception:
                logger.log_info('Retrying to approach the zone dep')
                self.__retry_move_robot_around_zone_dep()
                pass

    def __retry_move_robot_around_zone_dep(self):
        logger.log_info('Moving closer to approach the zone dep')
        (x, y) = self.robot_mover.move_closer_on_plane(self.zone_dep_cardinal)
        self.comm_pi.sendCoordinates(x, y)
        self.move_robot_around_zone_dep

    def drop_piece(self):
        logger.log_info('Drop the arm')
        time.sleep(0.5)
        self.comm_pi.moveArm('7800')
        time.sleep(0.5)
        self.comm_pi.changeCondensateurHigh()
        time.sleep(0.5)
        logger.log_info('Lifting the arm')
        self.comm_pi.moveArm('2000')

    def __detect_x_y_point_zone_dep(self):
        logger.log_info("Sequence to detect point")

        robot_img = self.comm_pi.getImage()
        height, width, channels = robot_img.shape
        x, y = detect_point_zone_dep(robot_img)

        logger.log_info('Drop piece, detected center of first point ' +
                        str(x) + ', ' + str(y))

        real_x, real_y = self.robot_mover.move_robot_from_embarked_referential(
            x, y, self.zone_dep_cardinal, width, height)

        return (real_x, real_y)

    def __move_to_point_zone_dep(self):
        if self.depot_number == ZONE_0:
            is_made_move = False
            while not is_made_move:
                (x, y) = self.__detect_x_y_point_zone_dep()

                if (y < -80):
                    is_made_move = False
                    self.comm_pi.sendCoordinates(0, -10)
                else:
                    self.comm_pi.sendCoordinates(round(x), round(y))
                    is_made_move = True

        elif self.depot_number == ZONE_1:
            for i in range(2):
                self.__try_send_move_to_zone_dep(i < 2 - 1)

        elif self.depot_number == ZONE_2:
            for i in range(3):
                self.__try_send_move_to_zone_dep(i < 3 - 1)

        elif self.depot_number == ZONE_3:
            for i in range(4):
                self.__try_send_move_to_zone_dep(i < 4 - 1)

        else:
            logger.log_critical(
                "No zone dep point given to Sequence to adjust movement...")
            raise Exception(
                "No zone dep given to adjust movement to drop piece")

    def __try_send_move_to_zone_dep(self, cond):
        is_made_move = False
        while not is_made_move:
            is_made_move = self.__send_move_to_zone_dep(cond)

    def __send_move_to_zone_dep(self, adjust):
        (x, y) = self.__detect_x_y_point_zone_dep()

        if (y < -80):
            self.comm_pi.sendCoordinates(0, -10)
            return False

        self.comm_pi.sendCoordinates(round(x), round(y))

        # self.__rotate_robot_on_zone_plane(self.zone_dep_cardinal, 3)

        if adjust:
            self.comm_pi.sendCoordinates(0, 0)

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

    def __rotate_robot_on_zone_dep(self):
        logger.log_info("Rotate on zone dep plane...")
        self.__rotate_robot_on_zone_plane(self.zone_dep_cardinal)

    def __rotate_robot_on_zone_pickup(self):
        logger.log_info("Rotate on pickup zone plane...")
        self.__rotate_robot_on_zone_plane(self.zone_pickup_cardinal)

    def __rotate_robot_on_zone_plane(self, cardinal_point, first_it=0):
        img = self.take_image()
        robot_detector = RobotDetector(img)
        robot_angle = robot_detector.find_angle_of_robot()

        self.__decision(EAST(), self.__rotate_to_east, robot_angle, first_it,
                        cardinal_point)
        self.__decision(SOUTH(), self.__rotate_to_south, robot_angle, first_it,
                        cardinal_point)
        self.__decision(WEST(), self.__rotate_to_west, robot_angle, first_it,
                        cardinal_point)
        self.__decision(NORTH(), self.__rotate_to_north, robot_angle, first_it,
                        cardinal_point)

    def __decision(self, cardinal, rotate_function, robot_angle, first_it,
                   cardinal_point):
        if cardinal_point == cardinal:
            logger.log_info("Rotate to " + cardinal + "...")
            rotate_function(robot_angle)
            if first_it < 3:
                logger.log_info('Correction angle ' + str(first_it))
                first_it = first_it + 2
                self.__rotate_robot_on_zone_plane(cardinal, first_it)

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

    def end_sequence(self):
        self.comm_pi.redLightOn()
        time.sleep(5)
