import pickle
import time
import cv2
import traceback
import sys

from infrastructure.communication_pi.comm_pi import Communication_pi
from test.LargeTest.mock.comm_pi import Communication_pi_mock
from test.LargeTest.mock.cap import Cap_mock
from sequence.Sequence import Sequence
from test.LargeTest.TestConstants import *

CANCER_MAC_USER = False

comm_pi = Communication_pi()


def connect(comm_pi):
    if comm_pi is None:
        return
    print("Now connecting...")
    comm_pi.connectToPi()
    time.sleep(5)


def calibrate():
    print("Calibration phase: ")
    pixel_to_xy_converter = None
    try:
        with open('calibration_data.pkl', 'rb') as input:
            pixel_to_xy_converter = pickle.load(input)

        return pixel_to_xy_converter
    except Exception as ex:
        print(ex)
        traceback.print_exc(file=sys.stdout)


def calibrateEmbark():
    pixel_to_xy_converter = None
    try:
        with open('calibration_embark.pkl', 'rb') as input:
            pixel_to_xy_converter = pickle.load(input)

        return pixel_to_xy_converter
    except Exception as ex:
        print(ex)
        traceback.print_exc(file=sys.stdout)


def main():
    cap = cv2.VideoCapture(1)
    if CANCER_MAC_USER:
        cap.set(3, 1600)
        cap.set(4, 1200)
        cap.set(3, 640)
        cap.set(4, 480)

    time.sleep(5)
    _, frame = cap.read()

    # cv2.imshow("TEST", frame)
    # cv2.waitKey()

    connect(comm_pi)
    pixel_to_xy_converter = calibrate()
    robot_cam_pixel_to_xy_converter = calibrateEmbark()

    # X_END = X_END_START
    # Y_END = Y_END_START

    # X_END = X_END_CHARGE
    # Y_END = Y_END_CHARGE

    sequence = Sequence(cap, comm_pi, pixel_to_xy_converter,
                        robot_cam_pixel_to_xy_converter)
    print("Go to start zone...")
    # sequence.set_end_point(X_END_START, Y_END_START)
    # sequence.start()
    # sequence.go_to_start_zone()
    print("Go to start charge station...")
    # sequence.go_to_c_charge_station()
    print("Go back from start charge station...")
    # sequence.go_back_from_charge_station()
    print("Go to qr...")
    # sequence.make_dat_dance_to_decode_qr_boy()
    # sequence.go_to_zone_dep()
    # sequence.go_to_zone_pickup()
    sequence.go_to_start_zone()
    sequence.end()
    print("Sad face we're done...")

    # sequence.go_to_zone_dep()


def main_test():
    # cap = Cap_mock()
    cap = cv2.VideoCapture(1)
    comm_pi = Communication_pi_mock()
    connect(comm_pi)
    pixel_to_xy_converter = calibrate()
    robot_cam_pixel_to_xy_converter = calibrateEmbark()

    # X_END = X_END_CHARGE
    # Y_END = Y_END_CHARGE

    sequence = Sequence(cap, comm_pi, pixel_to_xy_converter,
                        robot_cam_pixel_to_xy_converter)
    sequence.go_to_start_zone()


try:
    # main()
    main_test()
except KeyboardInterrupt:
    comm_pi.disconnectFromPi()
    print("bye")
    traceback.print_exc(file=sys.stdout)
