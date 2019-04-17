import cv2
import traceback
import sys
import time

from domain.pathfinding.Astar import Astar
from domain.pathfinding.PathSmoother import PathSmoother
from domain.image_analysis_pathfinding.PixelToXYCoordinatesConverter import *
from domain.image_analysis.ImageToGridConverter import *
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector
from domain.image_analysis.DetectBlurriness import *
from domain.image_analysis_pathfinding.RobotDetector import *
from domain.pathfinding.Exceptions.NoPathFoundException import *
from domain.pathfinding.Exceptions.NoBeginingPointException import *
from domain.QRCodeDictionnary import *
from util.Logger import Logger
from domain.image_analysis.Cardinal import *
from domain.RobotMover import *
from infrastructure.communication_ui.comm_ui import Communication_ui
from infrastructure.communication_ui.ui_destination import *
from domain.ObstacleDetector import *

from sequence.InitSequence import InitSequence
from sequence.PathSequence import PathSequence
from sequence.DrawSequence import *
from sequence.UtilSequence import *
from sequence.QRSequence import try_to_decode_qr
from sequence.ZoneDepSequence import *
from sequence.PickupZoneSequence import *
from sequence.ChargeSequence import *

DEBUG = False
SHOW_PATH = False
ROBOT_DANCE_X_POSITIVE = "50,0,0\n"
ROBOT_DANCE_X_NEGATIVE = "-50,0,0\n"

STRAT_1_Y_CODE_QR = 145
STRAT_2_Y_CODE_QR = 145
STRAT_3_Y_CODE_QR = 145

X_END_START_ZONE = 81
Y_END_START_ZONE = 121

Y_ARRAY_FOR_QR_STRATEGY = [120, 145, 170, 90]

X_RANGE_FOR_QR_STRATEGY = [200, 230, 260, 285]

logger = Logger(__name__)


class Sequence:
    def __init__(self,
                 image_taker,
                 comm_pi,
                 world_cam_pixel_to_xy_converter,
                 robot_cam_pixel_to_xy_converter,
                 no_world_cam=False):
        self.no_world_cam = no_world_cam
        self.image_taker = image_taker
        self.X_END = None
        self.Y_END = None
        self.comm_pi = comm_pi
        self.world_cam_pixel_to_xy_converter = world_cam_pixel_to_xy_converter
        self.robot_cam_pixel_to_xy_converter = robot_cam_pixel_to_xy_converter
        self.robot_mover = RobotMover(world_cam_pixel_to_xy_converter,
                                      robot_cam_pixel_to_xy_converter,
                                      image_taker)
        self.real_path = None
        self.starting_point = None
        self.smooth_path = None
        self.img = None
        self.piece_color = None
        self.depot_number = None
        self.piece_shape = None
        self.pathfinding_astar_retry = 0
        self.zone_dep_cardinal = None
        self.zone_dep_point = None
        self.zone_pickup_cardinal = None
        self.zone_pickup_point = None
        self.zone_start_point = None
        self.actual_robot_path = []
        self.actual_pathfinding_image = None
        self.validation_piece_taken_pickup_zone = True
        self.array_point_obstacle = []
        self.__init_sequence()
        self.__init_obstacle_point_array()
        self.comm_pi.moveArm('2000')

    def __init_sequence(self):
        self.comm_pi.changeCondensateurHigh()
        self.comm_pi.redLightOff()

        initSequence = InitSequence(X_END_START_ZONE, Y_END_START_ZONE,
                                    self.image_taker, self.no_world_cam)
        self.zone_start_point, self.zone_dep_cardinal, self.zone_dep_point, self.zone_pickup_cardinal, self.zone_pickup_point = initSequence.init(
        )

        img = self.take_image()

        cv2.circle(img, ((self.zone_dep_point[0] * 2),
                         (self.zone_dep_point[1] * 2)), 3, [0, 0, 255])
        cv2.circle(img, ((self.zone_pickup_point[0] * 2),
                         (self.zone_pickup_point[1] * 2)), 3, [0, 0, 255])
        cv2.circle(img, ((self.zone_start_point[0] * 2),
                         (self.zone_start_point[1] * 2)), 3, [0, 0, 255])

        # cv2.imshow('ok', img)
        # cv2.waitKey()

        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

    def __init_obstacle_point_array(self):
        img = self.take_image()

        obstacle_detector = ObstacleDetector(img)
        self.array_point_obstacle = obstacle_detector.find_center_of_obstacle()

    def start(self, scan_for_qr=False, unsecure=False):
        logger.log_info("## Starting path finding")
        create_done = self.__create_smooth_path(unsecure)

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

        if (create_done is None):
            return

        logger.log_info("## Rotating robot")
        self.__send_rotation_angle()

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

        logger.log_info("## Convert to X Y")
        self.__convert_to_xy(create_done)

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

        logger.log_info("## Send coordinates")
        self.__send_coordinates(create_done, scan_for_qr)

    def __create_smooth_path(self, unsecure=False):
        self.actual_pathfinding_image = self.take_image()
        logger.log_info('Pathfinding for point ' + str(self.Y_END) + ' ' +
                        str(self.X_END))
        pathSequence = PathSequence(self.pathfinding_astar_retry,
                                    self.actual_pathfinding_image, self.X_END,
                                    self.Y_END)
        return pathSequence.create_smooth_path(unsecure)

    def __convert_to_xy(self, smooth_path):
        self.real_path = self.world_cam_pixel_to_xy_converter.convert_to_xy(
            smooth_path)
        self.starting_point = self.real_path[0]
        self.real_path = self.real_path[1:]

    def __send_coordinates(self, smooth_path, scan_for_qr=False):
        actual_robot_path = [smooth_path[0]]
        for point in self.real_path:
            self.__send_rotation_angle(smooth_path)

            x_coord = int(round(point[0] - self.starting_point[0], 0))
            y_coord = int(round(point[1] - self.starting_point[1], 0))
            self.comm_pi.sendCoordinates(x_coord, y_coord)

            if scan_for_qr is True:
                imgqr = self.comm_pi.getImage()
                info_qr = try_to_decode_qr(imgqr)
                if (info_qr is not None):
                    self.piece_shape = info_qr['shape']
                    self.piece_color = info_qr['color']
                    self.depot_number = info_qr['zone']
                    self.comm_pi.scan_for_qr = False

                    comm_ui = Communication_ui()
                    comm_ui.SendImage(imgqr, EMBARKED_FEED_IMAGE())
                    break

            while True:
                try:
                    img = self.take_image()
                    center_and_image = find_current_center_robot(
                        img, smooth_path)

                    draw_robot_on_path_image(center_and_image['image'],
                                             actual_robot_path,
                                             center_and_image['center'])
                    self.starting_point = self.world_cam_pixel_to_xy_converter.convert_to_xy_point(
                        (center_and_image['center'][0],
                         center_and_image['center'][1]))
                    break
                except Exception as ex:
                    logger.log_error(ex)
                    logger.log_critical(traceback.format_exc())

    def __send_rotation_angle(self, path=None):
        while True:
            try:
                img = self.take_image()
                robot_detector = RobotDetector(img)
                robot_angle = robot_detector.find_angle_of_robot()
                turning_angle = int(round(robot_angle))
                if (abs(turning_angle) > 3):
                    self.comm_pi.sendAngle(turning_angle)
                break
            except Exception as ex:
                logger.log_error(ex)
                logger.log_debug(traceback.format_exc())

    def take_image(self):
        logger.log_info("Capture d'image de la camera monde en cours...")

        if (self.no_world_cam):
            self.img = cv2.imread('./testy.jpg')
            return self.img

        while True:
            ret, self.img = self.image_taker.read()
            if ret:
                break

        # comm_ui = Communication_ui()
        # comm_ui.SendImage(self.img, WORLD_FEED_IMAGE())

        return self.img

    def set_end_point(self, x, y):
        self.X_END = x
        self.Y_END = y

    def go_to_start_zone(self):
        comm_ui = Communication_ui()
        comm_ui.SendText('Going to start zone', SEQUENCE_TEXT())
        logger.log_info('Going to start zone')
        self.set_end_point(self.zone_start_point[0], self.zone_start_point[1])

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

        self.__try_go_to_decided_zone()

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

    def go_to_zone_pickup(self):
        comm_ui = Communication_ui()
        comm_ui.SendText('Going to zone pickup', SEQUENCE_TEXT())
        logger.log_info('Going to zone pickup')
        self.comm_pi.changeServoVert('6000')
        self.comm_pi.changeServoHori('2000')
        self.set_end_point(self.zone_pickup_point[0],
                           self.zone_pickup_point[1])

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

        self.__try_go_to_decided_zone()
        self.__rotate_robot_on_zone_pickup()

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

    def go_to_zone_dep(self):
        comm_ui = Communication_ui()
        comm_ui.SendText('Going to zone depôt', SEQUENCE_TEXT())
        logger.log_info('Going to zone depôt')
        self.set_end_point(self.zone_dep_point[0], self.zone_dep_point[1])

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

        self.__try_go_to_decided_zone()
        self.__rotate_robot_on_zone_dep()

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

    def __try_go_to_decided_zone(self):
        while True:
            try:
                self.start()
                break
            except (NoBeginingPointException, NoPathFoundException):
                logger.log_critical(traceback.format_exc())
                logger.log_critical("Ayoye je suis dans l'obstacle...")

                img = self.take_image()
                robot_detector = RobotDetector(img)
                robot_point = robot_detector.find_center_of_robot()
                robot_angle = robot_detector.find_angle_of_robot()

                x, y = self.robot_mover.get_out_of_object(
                    robot_angle, robot_point, self.array_point_obstacle)
                self.comm_pi.sendCoordinates(x, y)
                pass

    def __rotate_robot_on_zone_dep(self):
        logger.log_info("Rotate on zone dep plane...")
        rotate_robot_on_zone_plane(self.image_taker, self.zone_dep_cardinal,
                                   self.comm_pi)

    def __rotate_robot_on_zone_pickup(self):
        logger.log_info("Rotate on pickup zone plane...")
        rotate_robot_on_zone_plane(self.image_taker, self.zone_pickup_cardinal,
                                   self.comm_pi)

    def go_to_decode_qr(self):
        comm_ui = Communication_ui()
        comm_ui.SendText('Going to decode code QR', SEQUENCE_TEXT())
        self.comm_pi.changeServoVert('6000')
        self.comm_pi.changeServoHori('5500')

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

        self.comm_pi.scan_for_qr = True

        for y in Y_ARRAY_FOR_QR_STRATEGY:
            for x in X_RANGE_FOR_QR_STRATEGY:
                self.set_end_point(x, y)
                try:
                    self.start(self.comm_pi.scan_for_qr)
                    # img = self.__get_image_embarked()
                    # info_qr = try_to_decode_qr(img)
                    if self.comm_pi.scan_for_qr is False:
                        # self.piece_shape = info_qr['shape']
                        # self.piece_color = info_qr['color']
                        # self.depot_number = info_qr['zone']
                        img = self.take_image()
                        comm_ui = Communication_ui()
                        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

                        break
                except Exception as ex:
                    logger.log_error(ex)
                    logger.log_debug(traceback.format_exc())
                    logger.log_debug(
                        'Decode QR fallback to other point, obstacle in the way'
                    )
                    pass

            if self.comm_pi.scan_for_qr is False:
                break

    def snipe_qr(self):
        self.comm_pi.sendAngle(-35)
        self.comm_pi.changeServoVert('6000')
        self.comm_pi.changeServoHori('5500')
        img = self.comm_pi.getImageFullHD()

        if DEBUG:
            cv2.imshow("snipe", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        values = try_to_decode_qr(img)

        logger.log_info(values[ZONE] + ", " + values[COULEUR] + ", " +
                        values[PIECE])

    def go_to_charge_robot(self):
        comm_ui = Communication_ui()
        comm_ui.SendText('Going to charge robot', SEQUENCE_TEXT())

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

        chargeSequence = ChargeSequence(
            self.comm_pi, self.__send_rotation_angle,
            self.world_cam_pixel_to_xy_converter, self.image_taker)
        chargeSequence.start()

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

    def move_robot_around_pickup_zone(self, validation=True):
        pickupZoneSequence = PickupZoneSequence(
            validation, self.comm_pi, self.zone_pickup_cardinal,
            self.robot_cam_pixel_to_xy_converter, self.robot_mover,
            self.go_to_zone_pickup, self.piece_shape, self.piece_color)

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

        pickupZoneSequence.try_to_move_robot_around_pickup_zone()

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

        (x, y) = self.robot_mover.fallback_from_cardinality(
            self.zone_pickup_cardinal)

        img = self.take_image()
        comm_ui = Communication_ui()
        comm_ui.SendImage(img, WORLD_FEED_IMAGE())

        self.comm_pi.sendCoordinates(x, y)

    def move_robot_around_zone_dep(self):
        comm_ui = Communication_ui()
        comm_ui.SendText('Moving around zone depôt', SEQUENCE_TEXT())

        zoneDepSequence = ZoneDepSequence(self.depot_number, self.comm_pi,
                                          self.robot_mover,
                                          self.zone_dep_cardinal)
        while True:
            img = self.take_image()
            comm_ui = Communication_ui()
            comm_ui.SendImage(img, WORLD_FEED_IMAGE())

            zoneDepSequence.move_to_point_zone_dep()
            zoneDepSequence.drop_piece()

            img = self.take_image()
            comm_ui = Communication_ui()
            comm_ui.SendImage(img, WORLD_FEED_IMAGE())

            (x, y) = self.robot_mover.fallback_from_cardinality(
                self.zone_dep_cardinal)

            img = self.take_image()
            comm_ui = Communication_ui()
            comm_ui.SendImage(img, WORLD_FEED_IMAGE())

            if x == -1 and y == -1:
                logger.log_info('Retrying to approach the zone dep')
                zoneDepSequence.retry_move_robot_around_zone_dep()
            else:
                self.comm_pi.sendCoordinates(x, y)
                break

    def end_sequence(self):
        comm_ui = Communication_ui()
        comm_ui.SendText('Sequence is done', SEQUENCE_TEXT())
        self.comm_pi.redLightOn()

    def end(self):
        comm_ui = Communication_ui()
        comm_ui.SendText('Sequence is over and done', SEQUENCE_TEXT())
        comm_ui = Communication_ui()
        comm_ui.sendStopSignal()
        time.sleep(5)
