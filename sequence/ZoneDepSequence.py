import time
import traceback

from domain.QRCodeDictionnary import *
from domain.image_analysis.opencv_callable.DetectPointZoneDep import detect_point_zone_dep
from infrastructure.communication_ui.comm_ui import Communication_ui
from infrastructure.communication_ui.ui_destination import *
from util.Logger import Logger

logger = Logger(__name__)

class ZoneDepSequence:
    def __init__(self, depot_number, comm_pi, robot_mover, zone_dep_cardinal):
        self.depot_number = depot_number
        self.comm_pi = comm_pi
        self.robot_mover = robot_mover
        self.zone_dep_cardinal = zone_dep_cardinal

    def move_to_point_zone_dep(self):
        if self.depot_number == ZONE_0:
            self.__try_send_move_to_zone_dep(1)

        elif self.depot_number == ZONE_1:
            iteration = 2
            for i in range(iteration):
                self.__try_send_move_to_zone_dep(i < iteration - 1)

        elif self.depot_number == ZONE_2:
            iteration = 3
            for i in range(iteration):
                self.__try_send_move_to_zone_dep(i < iteration - 1)

        elif self.depot_number == ZONE_3:
            iteration = 4
            for i in range(iteration):
                self.__try_send_move_to_zone_dep(i < iteration - 1)

        else:
            logger.log_critical(
                "No zone dep point given to Sequence to adjust movement...")
            raise Exception(
                "No zone dep given to adjust movement to drop piece")
                
    def __try_send_move_to_zone_dep(self, cond):
        is_made_move = False
        while not is_made_move:
            is_made_move = self.__send_move_to_zone_dep()

    def __send_move_to_zone_dep(self):
        (x, y) = self.__detect_x_y_point_zone_dep()

        logger.log_info('DROP PIECE - Attempting a move to ' + str(x) + " " +
                        str(y))

        if (y < -80):
            logger.log_info('DROP PIECE - Y is too far, getting closer' +
                            str(y))
            self.comm_pi.sendCoordinates(0, -10)
            return False

        if (x > 20):
            logger.log_info('DROP PIECE - X is too far, getting closer ' +
                            str(x))
            self.comm_pi.sendCoordinates(10, 0)
            return False

        self.comm_pi.sendCoordinates(round(x), round(y))

        # self.__rotate_robot_on_zone_plane(self.zone_dep_cardinal, 3)

        return True
    
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

    def drop_piece(self):
        logger.log_info('Drop the arm')
        time.sleep(0.5)
        self.comm_pi.moveArm('7800')
        time.sleep(0.5)
        self.comm_pi.changeCondensateurHigh()
        time.sleep(0.5)
        logger.log_info('Lifting the arm')
        self.comm_pi.moveArm('2000')

    def retry_move_robot_around_zone_dep(self):
        logger.log_info('Moving closer to approach the zone dep')
        (x, y) = self.robot_mover.move_closer_on_plane(self.zone_dep_cardinal)
        self.comm_pi.sendCoordinates(x, y)
        # self.move_robot_around_zone_dep()