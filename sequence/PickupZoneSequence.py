import time
import traceback

from domain.image_analysis.Cardinal import *
from domain.image_analysis.opencv_callable.DetectPiece import detect_piece
from infrastructure.communication_ui.comm_ui import Communication_ui
from infrastructure.communication_ui.ui_destination import *
from util.Logger import Logger

logger = Logger(__name__)

NUMBER_OF_INCREMENT_PICKUP_ZONE = 20


class PickupZoneSequence:
    def __init__(self, validation, comm_pi, zone_pickup_cardinal,
                 robot_cam_pixel_to_xy_converter, robot_mover,
                 go_to_zone_pickup, piece_shape, piece_color):
        self.validation_piece_taken_pickup_zone = validation
        self.comm_pi = comm_pi
        self.zone_pickup_cardinal = zone_pickup_cardinal
        self.robot_cam_pixel_to_xy_converter = robot_cam_pixel_to_xy_converter
        self.robot_mover = robot_mover
        self.go_to_zone_pickup = go_to_zone_pickup
        self.piece_shape = piece_shape
        self.piece_color = piece_color

    def try_to_move_robot_around_pickup_zone(self):
        comm_ui = Communication_ui()
        comm_ui.SendText('Moving around pickup zone', SEQUENCE_TEXT())

        MOVEMENT_OFFSET = 20
        self.comm_pi.changeCondensateurLow()
        x_mm_movement_point = (MOVEMENT_OFFSET, 0)
        x_mm_movement_point_negative = (-1 * MOVEMENT_OFFSET, 0)
        y_mm_movement_point = (0, MOVEMENT_OFFSET)
        y_mm_movement_point_negative = (0, -1 * MOVEMENT_OFFSET)

        self.__decision_with_cardinal(SOUTH(), x_mm_movement_point_negative,
                                      -90)
        self.__decision_with_cardinal(NORTH(), x_mm_movement_point, 90)
        self.__decision_with_cardinal(EAST(), y_mm_movement_point_negative, 0)
        self.__decision_with_cardinal(WEST(), y_mm_movement_point, 180)

    def __decision_with_cardinal(self, cardinal, movement, angle):
        if self.zone_pickup_cardinal == cardinal:
            logger.log_info("Move around " + cardinal + " pick up...")
            self.__validate_if_pickup_sequence_is_done_and_move(
                movement, angle)

    def __validate_if_pickup_sequence_is_done_and_move(self, movement_point,
                                                       angle):
        piece_grabbed = False
        while piece_grabbed is False:
            piece_grabbed, real_x, real_y = self.__move_on_pickup_zone(
                movement_point, angle)

            if not self.validation_piece_taken_pickup_zone:
                break

            if piece_grabbed:
                validate_piece_was_grabbed = self.__validate_piece_taken(
                    real_x, real_y)
                if validate_piece_was_grabbed is False:
                    # WIP Refaire une seule itération
                    self.go_to_zone_pickup()
                    self.try_to_move_robot_around_pickup_zone()

                break

            (x, y) = self.robot_mover.fallback_from_cardinality(
                self.zone_pickup_cardinal)
            self.comm_pi.sendCoordinates(x, y)
            self.go_to_zone_pickup()

    def __validate_piece_taken(self, x, y):
        self.comm_pi.sendCoordinates(x * -1, y * -1.5)
        robot_img = self.comm_pi.getImage()
        robot_big_img = self.comm_pi.getImageFullHD()

        try:
            x, y = detect_piece(
                robot_img,
                robot_big_img,
                self.piece_shape,
                self.piece_color,
                validation=True)
            logger.log_critical("VALIDATE PIECE TAKEN - FOUND ONE...")
            return False
        except Exception:
            logger.log_critical("VALIDATE PIECE TAKEN - Yes we grabbed it...")
            logger.log_critical(traceback.format_exc())
            return True

    def __move_on_pickup_zone(self, moving_point, angle):
        number_of_increment = NUMBER_OF_INCREMENT_PICKUP_ZONE
        i = 0

        piece_grabbed = False
        real_x = 0
        real_y = 0
        while i < number_of_increment:
            if piece_grabbed is False and real_x == 0 and real_y == 0:
                x, y = self.robot_cam_pixel_to_xy_converter.convert_real_xy_given_angle(
                    moving_point, angle)
                self.comm_pi.sendCoordinates(x, y)

            piece_grabbed, real_x, real_y = self.__grab_piece()

            if piece_grabbed is False:
                self.comm_pi.sendCoordinates(real_x, real_y)

            if piece_grabbed:
                break

            i += 1
        return (piece_grabbed, real_x, real_y)

    def __grab_piece(self):
        logger.log_info("Trying to grab piece...")
        robot_img = self.comm_pi.getImage()
        robot_big_img = self.comm_pi.getImageFullHD()

        height, width, channels = robot_img.shape

        try:
            x, y = detect_piece(robot_img, robot_big_img, self.piece_shape,
                                self.piece_color)
            logger.log_info("Found piece!")
        except Exception:
            logger.log_critical(
                "Could not find piece, continuing to move to detect it...")
            logger.log_critical(traceback.format_exc())
            return False, 0, 0

        real_x, real_y = self.robot_mover.move_robot_from_embarked_referential(
            x, y, self.zone_pickup_cardinal, width, height)

        if real_y < -80:
            logger.log_critical("Piece point is too far : " + str(real_x) +
                                ", " + str(real_y))
            return False, 0, 0

        if (real_x > 20):
            logger.log_info('DROP PIECE - X is too far, getting closer ' +
                            str(x))
            return False, 10, 0

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
