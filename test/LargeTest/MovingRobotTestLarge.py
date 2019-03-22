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

CANCER_MAC_USER = True

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


def main():
    cap = cv2.VideoCapture(1)
    time.sleep(5)
    _, frame = cap.read()

    if CANCER_MAC_USER:
        cap.set(3, 1600)
        cap.set(4, 1200)

    # cv2.imshow("TEST", frame)
    # cv2.waitKey()

    connect(comm_pi)
    pixel_to_xy_converter = calibrate()

    # X_END = X_END_START
    # Y_END = Y_END_START

    # X_END = X_END_CHARGE
    # Y_END = Y_END_CHARGE

    sequence = Sequence(cap, comm_pi, pixel_to_xy_converter)
    # sequence.set_end_point(X_END, Y_END)
    sequence.go_to_start_zone()
    sequence.start()
    sequence.go_to_c_charge_station()
    sequence.go_to_c_back_from_charge_station()
    sequence.set_end_point(X_END_QR, Y_END_QR)
    sequence.start()
    sequence.dance_to_code_qr()
    sequence.end()

    # sequence.go_to_zone_dep()


def main_test():
    # cap = Cap_mock()
    cap = cv2.VideoCapture(1)
    comm_pi = Communication_pi_mock()
    connect(comm_pi)
    pixel_to_xy_converter = calibrate()

    # X_END = X_END_CHARGE
    # Y_END = Y_END_CHARGE

    sequence = Sequence(cap, comm_pi, pixel_to_xy_converter)
    sequence.go_to_start_zone()
    sequence.start()


try:
    main()
except KeyboardInterrupt:
    comm_pi.disconnectFromPi()
    print("bye")
    traceback.print_exc(file=sys.stdout)

# main_test()
