import unittest
from infrastructure.communication_pi.comm_pi import *


class commPiTest(unittest.TestCase):

    def setUp(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', 15555))
        self.server_socket.listen(1)

        self.comm_pi = Communication_pi("127.0.0.1", 15555)
        self.comm_pi.connectToPi()

        self.client, self.address = self.server_socket.accept()

    def test_when_send_coord_then_string_is_format_x_y_angle_backslashN(self):
        self.comm_pi.sendCoordinates(100, 50)

        self.comm_pi.disconnectFromPi()