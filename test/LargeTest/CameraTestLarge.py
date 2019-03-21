import time
from infrastructure.communication_pi.comm_pi import *


def test():

    comm = Communication_pi()
    comm.connectToPi()
    time.sleep(5)

    img = comm.getImage()
    time.sleep(5)

    cv2.imshow("test", img)

    comm.sendCoordinates("10, 10, 0")

test()