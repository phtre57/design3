import time

from util.Logger import Logger
from sequence.DrawSequence import draw_robot_on_image
from domain.image_analysis_pathfinding.RobotDetector import RobotDetector
from infrastructure.communication_ui.comm_ui import Communication_ui
from infrastructure.communication_ui.ui_destination import *

logger = Logger(__name__)

TENSION_THRESHOLD = 20

CHARGE_STATION_MOVE = (-370, -370)


class ChargeSequence:
    def __init__(self, comm_pi, send_rotation_angle,
                 world_cam_pixel_to_xy_converter, image_taker):
        self.comm_pi = comm_pi
        self.send_rotation_angle = send_rotation_angle
        self.world_cam_pixel_to_xy_converter = world_cam_pixel_to_xy_converter
        self.image_taker = image_taker
        self.img = None

    def start(self):
        decision_tension = self.__is_current_tension_too_high_to_charge()
        if (decision_tension):
            logger.log_info(
                "Robot already has that eletric feel now!! It is charged enough!"
            )
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

    def take_image(self):
        logger.log_info("Capture d'image de la camera monde en cours...")

        while True:
            ret, self.img = self.image_taker.read()
            if ret:
                break

        return self.img

    def __go_to_c_charge_station(self):
        self.send_rotation_angle()
        time.sleep(0.5)
        iteration = 7

        img = self.take_image()
        robot_detector = RobotDetector(img)
        robot_point = robot_detector.find_center_of_robot()
        actual_robot_path = [robot_point]

        for i in range(iteration):
            if (i % 2 == 0):
                self.send_rotation_angle()

            self.comm_pi.sendCoordinates(
                round(CHARGE_STATION_MOVE[0] / iteration),
                round(CHARGE_STATION_MOVE[1] / iteration))

            img = self.take_image()
            actual_robot_path = draw_robot_on_image(
                img, self.world_cam_pixel_to_xy_converter, actual_robot_path)

            time.sleep(0.2)

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

                if derivative_tension > 5:
                    break

                if tension > base_tension + 0.02:
                    base_tension = tension
                    derivative_tension += 1

            if tension > base_tension:
                break

            increment += 1

        comm_ui = Communication_ui()
        comm_ui.SendText('Charging robot now, electric feeeeel babyyy',
                         SEQUENCE_TEXT())
        logger.log_info("Charging robot waiting for that electric feel now...")

        while True:
            time.sleep(0.3)
            tension = self.comm_pi.getTension()
            logger.log_info('Tension now while charging ' + str(tension))
            if tension > 4 * 4 and tension < 30:
                tension = self.comm_pi.getTension()
                if tension > 4 * 4 and tension < 30:
                    break

        logger.log_info("Robot is charged now!")

    def __go_back_from_charge_station(self):
        img = self.take_image()
        robot_detector = RobotDetector(img)
        robot_point = robot_detector.find_center_of_robot()
        actual_robot_path = [robot_point]

        time.sleep(0.5)
        self.comm_pi.sendCoordinates(CHARGE_STATION_MOVE[0] * -1,
                                     CHARGE_STATION_MOVE[1] * -1)

        img = self.take_image()
        actual_robot_path = draw_robot_on_image(
            img, self.world_cam_pixel_to_xy_converter, actual_robot_path)

        time.sleep(1)
