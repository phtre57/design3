import unittest
import cv2
from infrastructure.communication_pi.comm_pi import *


class commPiTest(unittest.TestCase):
    def setUp(self):
        self.comm_pi = Communication_pi()

    def test_when_send_coord_then_string_is_format_x_y_angle_backslashN(self):
        # self.comm_pi.sendCoordinates(100, 50)
        # self.comm_pi.changeServoHori('5500')
        # self.comm_pi.changeServoVert('5500')
        self.comm_pi.moveArm('2000')


if __name__ == '__main__':
    unittest.main()
