import pickle
import time

from infrastructure.communication_pi.comm_pi import Communication_pi
from test.LargeTest.mock.comm_pi import Communication_pi_mock
from test.LargeTest.mock.cap import Cap_mock
from sequence.Sequence import Sequence
from test.LargeTest.TestConstants import *

def connect(comm_pi):
    if comm_pi is None:
        return
    print("Now connecting...")
    comm_pi.connectToPi()
    time.sleep(5)

def calibrate():
    print("Calibration phase: ")
    pixel_to_xy_converter = None

    with open('calibration_data.pkl', 'rb') as input:
        pixel_to_xy_converter = pickle.load(input)
    
    return pixel_to_xy_converter

def test_main_loop_move_robot(X_END, Y_END, sequence):
    print("## Starting path finding")
    sequence.create_smooth_path()

    print("## Rotating robot")
    sequence.send_rotation_angle()

    print("## Convert to X Y")
    sequence.convert_to_xy()

    print("## Send coordinates")
    sequence.send_coordinates()

def main():
    cap = cv2.VideoCapture(1)
    comm_pi = Communication_pi()
    connect(comm_pi)
    pixel_to_xy_converter = calibrate()
    sequence = Sequence(cap, X_END, Y_END, comm_pi)
    test_main_loop_move_robot(X_END_CHARGE, Y_END_CHARGE, sequence)
    test_main_loop_move_robot(X_END_CHARGE, Y_END_CHARGE, sequence)

    # test_main_loop_move_robot(X_END_QR, Y_END_QR)
    # test_main_loop_move_robot(X_END_PICKUP, Y_END_PICKUP)
    # test_main_loop_move_robot(X_END_DEPOT, Y_END_DEPOT)
    # test_main_loop_move_robot(X_END_START, Y_END_START)

    # test_main_loop_move_robot(274, 119)

    # test_main_loop_move_robot(X_END_TEST, Y_END_TEST)

    # test_main_loop_move_robot(X_1, Y_POINT)
    # test_main_loop_move_robot(X_2, Y_POINT)
    # test_main_loop_move_robot(X_3, Y_POINT)
    # test_main_loop_move_robot(X_4, Y_POINT)
    # test_main_loop_move_robot(X_5, Y_POINT)
    # test_main_loop_move_robot(X_6, Y_POINT)
    # test_main_loop_move_robot(X_7, Y_POINT)
    # test_main_loop_move_robot(X_8, Y_POINT)

def main_test():
    cap = Cap_mock()
    comm_pi = Communication_pi_mock()
    connect(comm_pi)
    pixel_to_xy_converter = calibrate()

    X_END = X_END_CHARGE
    Y_END = Y_END_CHARGE

    sequence = Sequence(cap, X_END, Y_END, comm_pi, pixel_to_xy_converter)
    test_main_loop_move_robot(X_END, Y_END, sequence)
    test_main_loop_move_robot(X_END, Y_END, sequence)

# main()
main_test()