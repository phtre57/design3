import socketio
import argparse
import cv2
import pickle
import traceback
import sys

from domain.image_analysis.ImageToGridConverter import *
from infrastructure.communication_pi.comm_pi import Communication_pi
from infrastructure.communication_ui.comm_ui import Communication_ui
from sequence.Sequence import Sequence
from util.Logger import Logger
from util.color import Color
from infrastructure.camera.TakeImage import TakeImage

CANCER_MAC_USER = False

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--d', dest='debug', type=bool, default=False, help='debug mode')
args = parser.parse_args()

comm_pi = Communication_pi()
logger = Logger(__name__)
image_taker = TakeImage(1, CANCER_MAC_USER)

def main_sequence(ui=True):
    image_taker.start()

    pixel_to_xy_converter = calibrate()
    robot_cam_pixel_to_xy_converter = calibrateEmbark()

    logger.log_info('Sequence start...')

    sequence = Sequence(image_taker, comm_pi, pixel_to_xy_converter, robot_cam_pixel_to_xy_converter)
    sequence.go_to_start_zone()
    sequence.go_to_c_charge_station()
    sequence.charge_robot_at_station()
    sequence.go_back_from_charge_station()
    sequence.go_to_decode_qr()
    sequence.piece_color = 'bleu'
    sequence.piece_shape = None
    sequence.depot_number = 'Zone 1'
    sequence.go_to_zone_pickup()
    sequence.move_robot_around_pickup_zone()
    sequence.go_to_zone_dep()
    sequence.move_robot_around_zone_dep()
    sequence.go_to_start_zone()

    sequence.end()
    image_taker.stop()

    logger.log_info('Sequence is done...')

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
