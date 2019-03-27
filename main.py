import socketio
import argparse
import cv2
import pickle
import time
import traceback
import sys

from domain.image_analysis.opencv_callable.DetectTable import detect_table
from domain.image_analysis.ImageToGridConverter import *
from domain.pathfinding.Astar import Astar
from test.domain.image_analysis.PathFindingImageTest import test_astar_on_image
from domain.image_analysis.opencv_callable.DetectQR import decode
from domain.image_analysis.opencv_callable.DetectContourPieces import detect_contour_pieces
from domain.image_analysis.opencv_callable.DetectZoneDep import detect_zone_dep
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
    frame = cv2.imread(path)

    test_image = ImageToGridConverter(frame, x, y)
    astar = Astar(test_image.grid, HEIGHT, LENGTH)
    astar.find_path()

    for point in astar.path:
        cv2.circle(test_image.image, (point.j, point.i), 1, [0, 0, 0])

    frame = test_image.image

    comm_ui = Communication_ui()
    comm_ui.SendImage(frame, "optpath")

    comm_ui = Communication_ui()
    comm_ui.SendImage(frame, "actualpath")

    cv2.imshow("main", frame)
    cv2.waitKey()


def main_sequence_old():
    pathfinding("./image_samples/real_image/globalmonde1.jpg", 240, 135)

    path = "./image_samples/real_image/qr.png"
    frame = cv2.imread(path)
    obj = decode(frame)

    comm_ui = Communication_ui()
    comm_ui.SendImage(frame, "actualimg")

    comm_ui = Communication_ui()
    comm_ui.SendText(obj.data, "qrcode")

    pathfinding("./image_samples/real_image/globalmonde1QR.jpg", 235, 60)

    path = "./image_samples/real_image/pieces.jpg"
    frame = cv2.imread(path)
    shape = detect_contour_pieces(frame)

    comm_ui = Communication_ui()
    comm_ui.SendImage(shape.frame, "actualimg")

    cv2.imshow('EDGES', shape.frame)
    cv2.waitKey()

    pathfinding("./image_samples/real_image/globalmonde1ZoneDep.jpg", 25, 122)

    path = "./image_samples/real_image/zonedep.jpg"
    frame = cv2.imread(path)
    shape = detect_zone_dep(frame)

    comm_ui = Communication_ui()
    comm_ui.SendImage(shape.frame, "actualimg")

    cv2.imshow('EDGES', shape.frame)
    cv2.waitKey()

    pathfinding("./image_samples/real_image/globalmonde1ZoneBlanche.jpg", 75,
                100)

    logger.log_info("Sequence done")

    init_conn_with_ui()


def start_cam():
    cap = cv2.VideoCapture(1)
    while True:
        if cap.isOpened():
            break
    return cap


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

    cap = start_cam()
    if CANCER_MAC_USER:
        cap.set(3, 1600)
        cap.set(4, 1200)
        cap.set(3, 640)
        cap.set(4, 480)

    _, frame = cap.read()

    connect(comm_pi)
    pixel_to_xy_converter = calibrate()
    robot_cam_pixel_to_xy_converter = calibrateEmbark()

    sequence = Sequence(cap, comm_pi, pixel_to_xy_converter,
                        robot_cam_pixel_to_xy_converter)
    logger.log_info('Sequence start...')
    sequence.go_to_start_zone()
    sequence.go_to_c_charge_station()
    sequence.charge_robot_at_station()
    sequence.go_back_from_charge_station()
    sequence.go_to_decode_qr()
    sequence.go_to_zone_pickup()
    sequence.rotate_robot_on_zone_pickup()
    sequence.move_robot_around_pickup_zone()
    sequence.go_to_zone_dep()
    sequence.rotate_robot_on_zone_dep()

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
