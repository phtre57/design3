import time

from util.Logger import Logger

logger = Logger(__name__)

TENSION_THRESHOLD = 11

CHARGE_STATION_MOVE = (-370, -370)


class ChargeSequence:
    def __init__(self, comm_pi, send_rotation_angle):
        self.comm_pi = comm_pi
        self.send_rotation_angle = send_rotation_angle

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

    def __go_to_c_charge_station(self):
        self.send_rotation_angle()
        time.sleep(0.5)
        iteration = 7
        for i in range(iteration):
            if (i % 2 == 0):
                self.send_rotation_angle()

            self.comm_pi.sendCoordinates(
                round(CHARGE_STATION_MOVE[0] / iteration),
                round(CHARGE_STATION_MOVE[1] / iteration))
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

                if tension > base_tension + 0.05:
                    derivative_tension += 1

            if tension > base_tension:
                break

            increment += 1

        logger.log_info("Charging robot waiting for that electric feel now...")

        while True:
            time.sleep(0.3)
            tension = self.comm_pi.getTension()
            logger.log_info('Tension now while charging ' + str(tension))
            if tension > 4 * 4:
                break

        logger.log_info("Robot is charged now!")

    def __go_back_from_charge_station(self):
        time.sleep(0.5)
        self.comm_pi.sendCoordinates(CHARGE_STATION_MOVE[0] * -1,
                                     CHARGE_STATION_MOVE[1] * -1)
        time.sleep(1)