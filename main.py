import socketio
import argparse
import cv2
import pickle
import time
import traceback
import sys

from infrastructure.communication_pi.comm_pi import Communication_pi
from infrastructure.communication_ui.comm_ui import Communication_ui
from sequence.Sequence import Sequence
from test.LargeTest.TestConstants import *
from util.Logger import Logger

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
    '--d', dest='debug', type=bool, default=False, help='debug mode')
args = parser.parse_args()

comm_pi = Communication_pi()

logger = Logger(__name__)

CANCER_MAC_USER = False


def connect(comm_pi):
    if comm_pi is None:
        return
    logger.log_info("Now connecting...")
    comm_pi.connectToPi()
    time.sleep(5)


def pathfinding(path, x, y):
    comm_ui = Communication_ui()
    comm_ui.SendImage(frame, "optpath")

    comm_ui = Communication_ui()
    comm_ui.SendImage(frame, "actualpath")


def main_sequence_old():
    comm_ui = Communication_ui()
    comm_ui.SendImage(frame, "actualimg")

    comm_ui = Communication_ui()
    comm_ui.SendText(obj.data, "qrcode")

    comm_ui = Communication_ui()
    comm_ui.SendImage(shape.frame, "actualimg")

    comm_ui = Communication_ui()
    comm_ui.SendImage(shape.frame, "actualimg")


def start_cam(open=True):
    logger.log_info("Ouverture de la caméra: ")
    if open:
        cap = cv2.VideoCapture(1)
        if CANCER_MAC_USER:
            cap.set(3, 640)
            cap.set(4, 480)

        while True:
            if cap.isOpened():
                break
        logger.log_info("Fin ouverture de la caméra: ")
        return cap
    return None


def calibrate():
    logger.log_info("Calibration World Cam phase: ")
    pixel_to_xy_converter = None
    try:
        with open('calibration_data.pkl', 'rb') as input:
            pixel_to_xy_converter = pickle.load(input)

        return pixel_to_xy_converter
    except Exception as ex:
        logger.log_info(ex)
        traceback.logger.log_info_exc(file=sys.stdout)


def calibrateEmbark():
    logger.log_info("Calibration Embark Cam phase: ")
    pixel_to_xy_converter = None
    try:
        with open('calibration_embark.pkl', 'rb') as input:
            pixel_to_xy_converter = pickle.load(input)

        return pixel_to_xy_converter
    except Exception as ex:
        logger.log_info(ex)
        traceback.logger.log_info_exc(file=sys.stdout)


def main_sequence(ui=True):

    cap = start_cam(False)

    # connect(comm_pi)

    pixel_to_xy_converter = calibrate()
    robot_cam_pixel_to_xy_converter = calibrateEmbark()

    sequence = Sequence(cap, comm_pi, pixel_to_xy_converter,
                        robot_cam_pixel_to_xy_converter, True)
    logger.log_info('Sequence start...')
    # sequence.go_to_start_zone()
    # sequence.go_to_c_charge_station()
    # sequence.charge_robot_at_station()
    # sequence.go_back_from_charge_station()
    # sequence.go_to_decode_qr()
    sequence.zone_dep_cardinal = 'EAST'
    sequence.piece_color = 'orange'
    sequence.piece_shape = None
    sequence.depot_number = 'Zone 3'
    # sequence.go_to_zone_pickup()
    # sequence.move_robot_around_pickup_zone()
    # sequence.go_to_zone_dep()
    sequence.move_robot_around_zone_dep()
    # sequence.go_to_start_zone()

    sequence.end()
    logger.log_info('Sequence is done...')

    # sequence.go_to_zone_dep()

    if (ui):
        init_conn_with_ui()


def init_conn_with_ui():
    logger.log_info("Waiting start signal")
    sio = socketio.Client()
    sio.connect('http://localhost:4000?token=MainRobot')

    @sio.on('validation')
    def on_validation(v):
        logger.log_info('disconnect MainRobot')
        sio.disconnect()

    @sio.on('start')
    def on_start(v):
        logger.log_info('Start signal')
        sio.emit("eventFromRobot", {
            'data': 'Started',
            'type': 'text',
            'dest': 'phase'
        })
        main_sequence()


def init_conn_without_ui():
    main_sequence(False)


def main():
    logger.increment_sequence_number()

    if (args.debug):
        logger.log_info("debug mode")
        init_conn_without_ui()
    else:
        logger.log_info("ui mode")
        init_conn_with_ui()


try:
    main()
except KeyboardInterrupt:
    comm_pi.disconnectFromPi()
    logger.log_info("bye")
    logger.log_critical(traceback.format_exc())
    cv2.destroyAllWindows()
