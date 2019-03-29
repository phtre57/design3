import time
from infrastructure.communication_pi.__comm_pi import *


def test():

    comm = Communication_pi()
    comm.connectToPi()
    time.sleep(5)

    start = time.time()
    img = comm.getImage()
    end = time.time()

    print(end - start)

    cv2.imshow("test", img)
    cv2.waitKey(0)

    comm.sendCoordinates("100,100,0\n")

    comm.disconnectFromPi()


test()